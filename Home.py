import streamlit as st
import pandas as pd
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kredi Skoru Sınıflandırma Uygulaması",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Başlık
st.title("📊 Kredi Skoru Sınıflandırma Uygulaması")

# Giriş ve yönlendirme açıklamaları
st.markdown("""
Merhaba! Bu uygulama, bireylerin finansal özelliklerine göre **kredi skoru sınıflandırması** yapar.
Farklı modelleme yöntemlerini kıyaslayabilir, veri setine dair içgörüler edinebilir ve sonuçları görselleştirebilirsiniz.

---

### 📌 Uygulama Sayfaları

- **Dataset Story**: Veri setinin yapısı, görselleştirmeler ve analiz hikayesi
- **Supervised Model**: Etiketli veriyle eğitilmiş model tahminleri
- **Semi Supervised Model**: Yarı denetimli (semi-supervised) modelle tahminler

👉 Lütfen sol menüden bir sayfa seçin.
""")

st.markdown("""
---

📍 Örnek kullanım senaryosu:

> 1. Dashboard sayfasına giderek veriyi inceleyin  
> 2. Ardından Supervised Model sayfasına geçerek test verisiyle bir skor tahmini yapın  
> 3. Son olarak Pseudo Label sayfasında modelin genel başarımını değerlendirin
""")

# Veri Seti Hikayesi
st.markdown("## 📖 Veri Seti Hikayesi")

st.markdown("""
### 💳 Veri Seti Tanımı

Bu veri seti, global bir finans şirketinin müşterilerine ait temel banka bilgileri ve krediye ilişkin finansal davranışlarını içermektedir. Şirket, yıllar içinde topladığı bu verileri kullanarak, bireyleri kredi skoru kategorilerine (Good, Standard, Poor) göre sınıflandırmayı amaçlamaktadır. Bu sınıflandırma, manuel değerlendirme süreçlerini azaltmak ve kredi risklerini daha etkin yönetmek için kullanılacaktır.

*Veri seti;*
- Müşterilerin yaş, gelir, maaş, kredi kartı sayısı, kredi başvuruları, borç durumu ve ödeme davranışları gibi çeşitli finansal özelliklerini içermektedir.
- Amaç, bireyleri kredi skoru aralıklarına otomatik olarak ayırabilen akıllı bir sınıflandırma sistemi geliştirmektir.

Bu yapı, kredi risk analizi, müşteri profilleme ve finansal karar destek sistemlerinde doğrudan kullanılabilir niteliktedir.
""")

# CSV veri yükleme ve gösterim
try:
    df = pd.read_csv("data/preprocessed_data.csv")  # ya da kendi yolun
    with st.expander("📂 Veri Setini Görüntüle"):
        st.dataframe(df)
except FileNotFoundError:
    st.error("❌ Veri seti bulunamadı. Lütfen doğru dosya yolunu kontrol edin.")

# Kredi Skoru açıklaması
st.markdown("""
### 📌 Kredi Skoru Nedir ve Neden Önemlidir?

Kredi skoru, bir kişinin finansal sağlığını ve kredi geri ödeme güvenilirliğini gösteren sayısal bir değerdir. Bankalar ve kredi kuruluşları, kredi vermeden önce kişilerin kredi skorlarını dikkate alır ve skorun düşük olması halinde kredi reddi veya yüksek faiz oranları uygulanabilir.

Bu veri seti, 100,000 müşterinin finansal davranışlarını ve kredi skorlarını içermektedir. Bu veriler, müşterilerin kredi skorlarını etkileyen faktörleri anlamamıza yardımcı olmaktadır.

*Veri Setindeki Kredi Skorları:*
- **Good (İyi)**: Yüksek kredi skoru, finansal davranışların çok iyi olduğunu gösterir
- **Standard (Standart)**: Orta düzey kredi skoru, genel olarak iyi finansal davranışları gösterir
- **Poor (Zayıf)**: Düşük kredi skoru, finansal davranışların iyileştirilmesi gerektiğini gösterir
""")

# Veri sözlüğü
with st.expander("📘 Veri Sözlüğü (Sütun Açıklamaları)"):
    st.markdown("""
    | Sütun Adı | Açıklama |
    |-----------|----------|
    | Age | Kişinin yaşı |
    | Annual_Income | Yıllık gelir (USD) |
    | Monthly_Inhand_Salary | Aylık elde edilen maaş (USD) |
    | Num_Bank_Accounts | Sahip olunan banka hesabı sayısı |
    | Num_Credit_Card | Sahip olunan kredi kartı sayısı |
    | Interest_Rate | Kredi faiz oranı (%) |
    | Num_of_Loan | Aktif kredi sayısı |
    | Delay_from_due_date | Son ödeme tarihinden sonraki gecikme günü |
    | Num_of_Delayed_Payment | Gecikmiş ödeme sayısı |
    | Changed_Credit_Limit | Kredi limitindeki değişiklik miktarı |
    | Num_Credit_Inquiries | Son 6 ayda yapılan kredi başvuru sayısı |
    | Outstanding_Debt | Ödenmemiş toplam borç |
    | Credit_Utilization_Ratio | Kredi kullanım oranı (%) |
    | Credit_History_Age | Kredi geçmişi süresi (ay) |
    | Payment_of_Min_Amount | Minimum ödeme yapılıp yapılmadığı (0=Hayır, 1=Evet, -1=Bilinmiyor) |
    | Total_EMI_per_month | Aylık toplam taksit ödemesi |
    | Amount_invested_monthly | Aylık yatırım miktarı |
    | Monthly_Balance | Aylık kalan bakiye |
    | Credit_Score | Kredi skoru (Good, Standard, Poor) |
    | Occupation_label | Meslek kodu |
    | Payment_Behaviour_Mapped | Ödeme davranışı kodu |
    | Credit_Mix_Mapped | Kredi karışımı kodu |
    | Auto Loan, Mortgage Loan, Student Loan, ... | Kredi türleri (one-hot encoded) |
    """)
