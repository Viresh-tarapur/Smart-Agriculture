import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

CSV_PATH = "Kharif_Seed_Distribution_KODI_2021-22_0.csv"

model = None
df_grouped = None
le_district = None
le_taluk = None
le_crop = None
df_original = None

def init_model():
    global model, df_grouped, le_district, le_taluk, le_crop, df_original
    if not os.path.exists(CSV_PATH):
        print(f"Warning: {CSV_PATH} not found. Smart Crop Advisor ML model will not be initialized.")
        return False
        
    try:
        df = pd.read_csv(CSV_PATH)
        df.columns = df.columns.str.strip()
        
        for col in df.columns:
            if "Seed Name" in col:
                df.rename(columns={col: "Crop"}, inplace=True)
            elif "District Name" in col:
                df.rename(columns={col: "District"}, inplace=True)
            elif "Taluk Name" in col:
                df.rename(columns={col: "Taluk"}, inplace=True)
            elif "GENERAL" in col:
                df.rename(columns={col: "General"}, inplace=True)
            elif "SCP" in col:
                df.rename(columns={col: "SCP"}, inplace=True)
            elif "TSP" in col:
                df.rename(columns={col: "TSP"}, inplace=True)
        
        required_cols = ["Crop", "District", "Taluk", "General", "SCP", "TSP"]
        for col in required_cols:
            if col not in df.columns:
                print(f"Missing column: {col}")
                return False
                
        df.fillna(0, inplace=True)
        df["General"] = pd.to_numeric(df["General"], errors="coerce")
        df["SCP"] = pd.to_numeric(df["SCP"], errors="coerce")
        df["TSP"] = pd.to_numeric(df["TSP"], errors="coerce")
        df.fillna(0, inplace=True)
        
        df["Total_Sales"] = df["General"] + df["SCP"] + df["TSP"]
        df = df[df["Total_Sales"] > 0]
        df["Crop"] = df["Crop"].astype(str).str.strip().str.upper()
        df["District"] = df["District"].astype(str).str.strip().str.title()
        df["Taluk"] = df["Taluk"].astype(str).str.strip().str.title()
        
        df_original = df.copy()
        
        df_grouped = df.groupby(["District", "Taluk", "Crop"])["Total_Sales"].sum().reset_index()
        
        le_district = LabelEncoder()
        le_taluk = LabelEncoder()
        le_crop = LabelEncoder()
        
        df_grouped["District_enc"] = le_district.fit_transform(df_grouped["District"])
        df_grouped["Taluk_enc"] = le_taluk.fit_transform(df_grouped["Taluk"])
        df_grouped["Crop_enc"] = le_crop.fit_transform(df_grouped["Crop"])
        
        X = df_grouped[["District_enc", "Taluk_enc", "Crop_enc"]]
        y = df_grouped["Total_Sales"]
        
        # In a real app we might cache the trained model to a file so we don't retrain on start
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X, y)
        print("ML fallback model ready!")
        return True
    except Exception as e:
        print(f"Error initializing Smart Crop Advisor model: {e}")
        return False

# Initialize the model on first load if the CSV exists
init_model()

def recommend_seeds_correct(district, taluk, top_n=5):
    if df_original is None:
        return None
        
    district = district.title()
    taluk = taluk.title()

    filtered = df_original[
        (df_original["District"] == district) &
        (df_original["Taluk"] == taluk)
    ]

    if filtered.empty:
        return None

    result = (
        filtered.groupby("Crop")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result.head(top_n)

def recommend_seeds_ml(district, taluk, top_n=5):
    if model is None or df_grouped is None:
        return None
        
    district = district.title()
    taluk = taluk.title()

    if district not in le_district.classes_ or taluk not in le_taluk.classes_:
        return None

    district_enc = le_district.transform([district])[0]
    taluk_enc = le_taluk.transform([taluk])[0]

    results = []

    for crop in df_grouped["Crop"].unique():
        crop_enc = le_crop.transform([crop])[0]

        input_df = pd.DataFrame({
            "District_enc": [district_enc],
            "Taluk_enc": [taluk_enc],
            "Crop_enc": [crop_enc]
        })

        pred = model.predict(input_df)[0]
        results.append((crop, round(pred, 2)))

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results[:top_n]

def smart_recommendation(district, taluk):
    # Ensure model is initialized or try to initialize if CSV is newly added
    if model is None:
        success = init_model()
        if not success:
            return None, "Model not initialized. Please ensure the dataset CSV is available."
            
    result = recommend_seeds_correct(district, taluk)

    if result is not None:
        # Convert pandas Series to dict
        recommendations = []
        for crop, value in result.items():
            recommendations.append({"crop": crop, "value": round(value, 2)})
        return recommendations, "Success"

    # ML fallback
    ml_result = recommend_seeds_ml(district, taluk)
    if ml_result is not None:
        recommendations = []
        for crop, value in ml_result:
            recommendations.append({"crop": crop, "value": value})
        return recommendations, "Success"
        
    return None, "No specific data or ML prediction available for this District and Taluk."
