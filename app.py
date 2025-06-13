
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import asyncio
# !!EKLENENLER!!

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from prophet import Prophet
# !!BİTİŞ!!

# === Sabitler ===
KWH_TO_TL_RATE = 2.5
CARBON_EMISSION_FACTOR_PER_KWH = 0.45

# === VERİ OLUŞTURMA ===
device_specs = {
    'Buzdolabı': {'brands': ['Arçelik', 'Beko', 'Bosch', 'Samsung'], 'avg_hourly_kwh': {'Arçelik': 0.12, 'Beko': 0.11, 'Bosch': 0.13, 'Samsung': 0.14}},
    'Klima': {'brands': ['Mitsubishi', 'Samsung', 'Arçelik', 'Vestel'], 'avg_hourly_kwh': {'Mitsubishi': 2.5, 'Samsung': 2.8, 'Arçelik': 2.6, 'Vestel': 2.4}},
    'Fırın': {'brands': ['Arçelik', 'Bosch', 'Siemens', 'Vestel'], 'avg_hourly_kwh': {'Arçelik': 1.8, 'Bosch': 2.0, 'Siemens': 1.9, 'Vestel': 1.7}}
}

np.random.seed(42)
data = []
for device, specs in device_specs.items():
    for brand in specs['brands']:
        for _ in range(10):
            usage_hours = np.random.uniform(1, 10)
            consumption = usage_hours * specs['avg_hourly_kwh'][brand] * np.random.uniform(0.9, 1.1)
            data.append([device, brand, usage_hours, consumption])

df_device_data = pd.DataFrame(data, columns=['Cihaz', 'Marka', 'Kullanım_süresi_saat', 'Tüketim_kWh'])

# ZAMAN SERİSİ İLE TARİH OLUŞTURULDU
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(730)]

# SICAKLIK VERİSİ KISMI
temp_vals = (15 + 15 * np.sin(np.linspace(0, 4 * np.pi, 730))).round(1)

# GÜNLÜK ENERJİ VERİSİ KISMI
base_kwh = 15
total_kwh = []

for i, date in enumerate(dates):
    weekday = date.weekday()
    temp = temp_vals[i]
    temp_effect = 0
    if temp < 10:
        temp_effect = (10 - temp) * 0.8
    elif temp > 25:
        temp_effect = (temp - 25) * 1.2
    if weekday >= 5:
        temp_effect += base_kwh * 0.15
    noise = np.random.normal(0, 2)
    daily = base_kwh + temp_effect + noise
    total_kwh.append(max(0, daily))

df_time_series = pd.DataFrame({
    'ds': dates,
    'temperature': temp_vals,
    'y': total_kwh
})
df_time_series['weekday'] = df_time_series['ds'].dt.day_name()

# === Streamlit kısmı ===
st.set_page_config(layout="wide")

# 1. Başlık ve geniş görünüm 
st.title("🔌 Geleceğin Evi: Gerçek Zamanlı Enerji Dashboard")

# === 2.Başlık: Geleceğin Evi - Cihaz Tüketim Tahmini ===
st.markdown("## 🔌 Geleceğin Evi 💡")
st.caption("Akıllı Enerji Kullanımı Tahmin ve Tasarruf Sistemi")

cihaz_listesi = [
    'Klima', 'Telefon Şarjı', 'Airfryer', 'Ütü', 'Süpürge',
    'TV', 'Buzdolabı', 'Bulaşık Makinesi', 'Çamaşır Makinesi', 'Fırın'
]
marka_listesi = ['Mitsubishi', 'Vestel', 'Samsung', 'Beko', 'Altus', 'Arçelik']
cihaz_kwh_degerleri = {
    'Klima': 2.5,
    'Telefon Şarjı': 0.01,
    'Airfryer': 1.4,
    'Ütü': 2.0,
    'Süpürge': 1.2,
    'TV': 0.1,
    'Buzdolabı': 0.12,
    'Bulaşık Makinesi': 1.3,
    'Çamaşır Makinesi': 1.5,
    'Fırın': 1.8
}
selected_device_single = st.selectbox("Cihaz Tipi", cihaz_listesi)
selected_brand_single = st.selectbox("Marka Seçiniz", marka_listesi)
usage_hours_single = st.number_input("Kullanım Süresi (saat)", min_value=0.5, max_value=24.0, value=1.0, step=0.5)



    # !!EKLENEN REGRASYON KISMI!!
if st.button("🔎 Enerji Tüketimini Tahmin Et"):
    # butona basılınca veriler işleniyor.


    # 🌟 Sabit katsayıya dayalı tüketım hesaplama(cihaz*süresi=kwh)
    estimated_kwh = usage_hours_single * cihaz_kwh_degerleri[selected_device_single]  # cihazın saatlik tüketim#
    estimated_tl = estimated_kwh * KWH_TO_TL_RATE                                      #elektrik faturası#
    carbon_footprint = round(estimated_kwh * CARBON_EMISSION_FACTOR_PER_KWH, 2)

    # VERİMLİLİK SKORU(Ortalama cihaz tüketimiyle kıyaslanarak verimlilik oranı çıkarıldı.)
    avg_consumption = df_device_data["Tüketim_kWh"].mean()
    efficiency_ratio = estimated_kwh / avg_consumption

    # ISRAF SKORU 
    waste_score = int(max(0, min(100, 100 - (efficiency_ratio * 100))))

    st.success(f"✅ {selected_device_single} ({selected_brand_single}) için tahmini tüketim:")
    st.markdown(f"- ⚡ **{estimated_kwh:.2f} kWh**")
    st.markdown(f"- 💸 **{estimated_tl:.2f} TL**")
    st.markdown(f"- 🌱 **{carbon_footprint} kg CO₂e** karbon ayak izi")
    st.markdown(f"- ♻️ **İsraf Skoru:** {waste_score}/100 _(ortalama tüketime göre)_")

    # 🤖 ML Regresyon  Tahmin KISMI
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import make_pipeline
    # burada df_device_data kulanılarak cihaz,marka ve süreye göre enerji tahmni yapılıyor.


    # Modeli oluştur ve eğit
    X = df_device_data[['Cihaz', 'Marka', 'Kullanım_süresi_saat']]
    y = df_device_data['Tüketim_kWh']

    model = make_pipeline(
        OneHotEncoder(handle_unknown='ignore'),
        LinearRegression()
    )
    model.fit(X, y)

    # Kullanıcının girişine göre tahmin
    input_df = pd.DataFrame([[selected_device_single, selected_brand_single, usage_hours_single]],
                            columns=['Cihaz', 'Marka', 'Kullanım_süresi_saat'])
    ml_kwh = model.predict(input_df)[0]
    ml_tl = ml_kwh * KWH_TO_TL_RATE

    # Sonucu göster
    st.markdown("### 🔎 ML Modeli ile Tahmin:")
    st.markdown(f"- 🔌 **{ml_kwh:.2f} kWh**")
    st.markdown(f"- 💵 **{ml_tl:.2f} TL** _(regresyon modeliyle tahmin)_")


# !!BİTİŞİ!!

    estimated_kwh = usage_hours_single * cihaz_kwh_degerleri[selected_device_single]
    estimated_tl = estimated_kwh * KWH_TO_TL_RATE
    carbon_footprint = round(estimated_kwh * CARBON_EMISSION_FACTOR_PER_KWH, 2)

    avg_consumption = df_device_data["Tüketim_kWh"].mean()
    efficiency_ratio = estimated_kwh / avg_consumption

    # Eğer senin tüketimin ortalamanın üzerindeyse, skor düşer/Eğer tüketimin ortalamanın altındaysa, skor artar.
    waste_score = int(max(0, min(100, 100 - (efficiency_ratio * 100))))

    st.success(f"✅ {selected_device_single} ({selected_brand_single}) için tahmini tüketim:")
    st.markdown(f"- ⚡ **{estimated_kwh:.2f} kWh**")
    st.markdown(f"- 💸 **{estimated_tl:.2f} TL**")
    st.markdown(f"- 🌱 **{carbon_footprint} kg CO₂e** karbon ayak izi")
    st.markdown(f"- ♻️ **İsraf Skoru:** {waste_score}/100 _(ortalama tüketime göre)_")

# === Grafikler ===

# Tarih kolonları
df_time_series["year"] = df_time_series["ds"].dt.year
df_time_series["month"] = df_time_series["ds"].dt.month_name()
df_time_series["month_num"] = df_time_series["ds"].dt.month  # sıralama için

st.subheader("📈 Enerji Tüketimi Analizleri")

# 1️⃣ YILLIK TOPLAM TÜKETİM
st.markdown("### 📅 Yıllık Toplam Tüketim")
yearly_total = df_time_series.groupby("year")["y"].sum().reset_index()
fig_yearly, ax_yearly = plt.subplots()
sns.barplot(data=yearly_total, x="year", y="y", ax=ax_yearly, palette="Blues")
ax_yearly.set_ylabel("Toplam Tüketim (kWh)")
st.pyplot(fig_yearly)

# 2️⃣ AYLIK ORTALAMA TÜKETİM
st.markdown("### 🗓️ Aylık Ortalama Tüketim")
monthly_avg = df_time_series.groupby(["month_num", "month"])["y"].mean().reset_index().sort_values("month_num")
fig_monthly, ax_monthly = plt.subplots()
sns.barplot(data=monthly_avg, x="month", y="y", ax=ax_monthly, palette="Oranges")
ax_monthly.set_ylabel("Ortalama Tüketim (kWh)")
ax_monthly.set_xticklabels(ax_monthly.get_xticklabels(), rotation=45)
st.pyplot(fig_monthly)

# 3️⃣ GÜNLÜK TÜKETİM ZAMAN SERİSİ
st.markdown("### 🗓️Günlük Enerji Tüketimi")
fig_daily, ax_daily = plt.subplots(figsize=(12, 4))
sns.lineplot(data=df_time_series, x="ds", y="y", ax=ax_daily, color="green")
ax_daily.set_ylabel("Tüketim (kWh)")
ax_daily.set_xlabel("Tarih")
st.pyplot(fig_daily)

# 4️⃣ HAFTALIK TÜKETİM (GÜNLERE GÖRE)
st.markdown("### 🗓️ Haftalık Tüketim Dağılımı")
fig_weekday, ax_weekday = plt.subplots()
sns.boxplot(data=df_time_series, x='weekday', y='y',
            order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            ax=ax_weekday, palette="Purples")

# Kutu grafiği (boxplot) ile haftanın hangi gününde ne kadar tüketim yapıldığını gösterir.
# Median, minimum, maksimum ve uç değerleri içerir.

ax_weekday.set_ylabel("Tüketim (kWh)")
ax_weekday.set_xlabel("Gün")
st.pyplot(fig_weekday)

# 5️⃣ SICAKLIK vs TÜKETİM
st.markdown("### 🌡️ Sıcaklık vs Tüketim")
fig_temp, ax_temp = plt.subplots()
sns.scatterplot(data=df_time_series, x="temperature", y="y", ax=ax_temp, color="orange", alpha=0.6)
sns.regplot(data=df_time_series, x="temperature", y="y", scatter=False, color="red", ax=ax_temp)

# Kırmızı çizgi: Regresyon (ilişki) çizgisi
# Buradan sıcaklık arttıkça veya azaldıkça tüketimin nasıl değiştiği analiz edilir.

ax_temp.set_xlabel("Sıcaklık (°C)")
ax_temp.set_ylabel("Tüketim (kWh)")
st.pyplot(fig_temp)

# 6️⃣ CİHAZ BAZLI ORTALAMA TÜKETİM
st.markdown("### 📈 Cihaz Bazlı Ortalama Tüketim Karşılaştırması")
avg_by_device = df_device_data.groupby("Cihaz")["Tüketim_kWh"].mean().sort_values()
fig_device, ax_device = plt.subplots()
# yatay çubuk grfaıgı ile cihazlar karşılaştırılır
sns.barplot(x=avg_by_device.values, y=avg_by_device.index, ax=ax_device, palette="Greens")
ax_device.set_xlabel("Ortalama Tüketim (kWh)")
st.pyplot(fig_device)


# !!PROPHET MODELİ İLE TAHMİN!!!

from prophet import Prophet

st.markdown("### 🔎  Prophet ile 30 Günlük Tüketim Tahmini")

# PROPHET İLE 30 GÜNLÜK ENERJI TAHMİNİ
# Prophet formatı: ds - y
df_prophet = df_time_series[['ds', 'y']].copy()

m = Prophet()
m.fit(df_prophet)
# model eğitimi yapmak için kullanıldı.

future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)

fig_forecast = m.plot(forecast)
st.pyplot(fig_forecast)


# !!BİTİŞİ!!



# !!CHATBOT KISMI!!
with st.sidebar.expander("🔎  Enerji Asistanı", expanded=False):
    user_prompt = st.text_input("Bir soru sorun (örn. 'Dün ne kadar enerji harcadım?')")

    async def query_llm_for_energy_insights(user_prompt):
        p = user_prompt.lower()
        anomaly_detected = np.random.rand() < 0.2
        waste_kwh = np.random.uniform(3, 10) if anomaly_detected else 0
        energy = {
            "yesterday_kwh": df_time_series['y'].iloc[-1].round(2),
            "last_week_avg_kwh": df_time_series['y'].tail(7).mean().round(2),
            "anomaly_detected": anomaly_detected,
            "simulated_waste_kwh": round(waste_kwh, 2),
            "monetary_loss_tl": round(waste_kwh * KWH_TO_TL_RATE, 2),
            "most_consuming_device": "Klima",
            "klima_brand": "Arçelik",
            "klima_avg_kwh_per_hour": 2.6,
            "possible_savings_kwh": round(df_time_series['y'].mean() * 0.15, 2),
            "current_carbon_footprint_kgco2e": round(df_time_series['y'].iloc[-1] * CARBON_EMISSION_FACTOR_PER_KWH, 2)
        }
        if "dün" in p:
            return f"Dün {energy['yesterday_kwh']} kWh tükettiniz. Haftalık ortalama {energy['last_week_avg_kwh']} kWh."
        elif "cihaz" in p:
            return f"En çok tüketim yapan cihaz: {energy['most_consuming_device']} ({energy['klima_brand']}) - {energy['klima_avg_kwh_per_hour']} kWh/saat."
        elif "tasarruf" in p:
            return f"Yaklaşık {energy['possible_savings_kwh']} kWh tasarruf edebilirsiniz."
        elif "israf" in p or "zarar" in p:
            if energy['monetary_loss_tl'] > 0:
                return f"Anomali tespit edildi! Tahmini kaybınız: {energy['monetary_loss_tl']} TL."
            else:
                return "Anormal bir durum tespit edilmedi."
        elif "karbon" in p:
            return f"Dünkü karbon ayak iziniz: {energy['current_carbon_footprint_kgco2e']} kg CO2e."
        else:
            return "Daha fazla bilgi için daha net sorular sorabilirsiniz."

    if user_prompt:
        with st.spinner("Yanıt getiriliyor..."):
            response = asyncio.run(query_llm_for_energy_insights(user_prompt))
            st.success(response)













