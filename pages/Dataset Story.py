import streamlit as st
import pandas as pd
import plotly.express as px  # type: ignore
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Kredi Skoru Analizi", layout="wide")

# Renk paleti tanımlamaları
color_palette = px.colors.sequential.PuBu_r  ## kategorik veriler için renk paleti
color_continuous_scale = px.colors.cyclical.Twilight  ## sayısal veriler için renk paleti

# # Hikaye başlığı ve giriş
st.title("📊 Kredi Skorumuz Hikayesi")
st.markdown("""
Bu proje kapsamında kullanılan veri seti, bireylerin kredi skorunu etkileyen finansal, 
demografik ve davranışsal değişkenleri içermektedir. Veri seti, farklı meslek gruplarına
mensup bireylerin zaman içerisindeki gelir-gider durumlarını, kredi kullanım alışkanlıklarını ve 
borçlanma eğilimlerini inceleyerek kredi skorlarını anlamaya yönelik bir temel sunmaktadır.
""")
st.header("📂 Veri Setinin İçeriği")
st.markdown("""
Veri setinde toplamda 37 sütun bulunmaktadır. Sütunlar genel olarak şu kategorilere ayrılabilir:.
""")
st.subheader("👤 Demografik Değişkenler")
st.markdown("""
- Month (Ay): Her gözlemin ait olduğu ay.     
- Age (Yaş): Bireyin yaşı.
- Occupation (Meslek): Bireyin mesleği (örneğin: Scientist, Teacher, Engineer).
""")
st.subheader("💰 Gelir ve Gider Verileri")
st.markdown("""
- Annual_Income: Bireyin yıllık brüt geliri (USD).
- Monthly_Inhand_Salary: Vergiler ve kesintiler sonrası net maaş.
- Total_Monthly_Expenses: Aylık toplam harcamalar.
""")
st.subheader("🏦 Bankacılık ve Kredi Kullanımı")
st.markdown("""
- Num_Bank_Accounts: Açık banka hesaplarının sayısı
- Num_Credit_Card: Aktif kredi kartı sayısı.
- Interest_Rate: Alınan kredilere uygulanan faiz oranı.
- Num_of_Loan: Alınan toplam kredi sayısı.
""")
st.subheader("⏳ Borç Davranışı ve Ödeme Alışkanlıkları")
st.markdown("""
- Delay_from_due_date: Ödemelerdeki gecikme süresi (gün).
- Outstanding_Debt: Ödenmemiş borç miktarı.
- Amount_invested_monthly: Aylık yatırım tutarı.
- EMI: Aylık ödenen kredi taksiti (Equated Monthly Installment).
""")
st.subheader("💳 Kredi Türleri Değişkenleri Açıklaması")
st.markdown("""
- Auto Loan: Bireyin taşıt kredisi kullanıp kullanmadığı
- Student Loan: Öğrenci kredisi alıp almadığı.
- Mortgage Loan: Konut kredisi (ev alımı veya ipotekli kredi) kullanıp kullanmadığı
- Credit-Builder Loan: Kredi skoru geliştirme kredisi kullanımı
- Debt Consolidation Loan: Borç birleştirme kredisi kullanımı.
- Home Equity Loan: Ev teminatlı kredi alıp almadığı.
- Payday Loan: Günlük kredi veya maaş günü kredisi alıp almadığı.
- Personal Loan: Kişisel kredi kullanıp kullanmadığı (bireysel ihtiyaçlar için).
- Not Specified: Kullanıcı bu bilgi alanını boş bırakmış ya da sistem bu bilgiyi kaydetmemiş.
""")

# Stil tanımlamaları - bölüm ayrımları ve kartlar için
css = """
<style>
    /* Bölüm başlıkları için stil */
    .section-header {
        background-color: rgba(28, 131, 225, 0.1);
        border-left: 4px solid #00d1d8;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin: 30px 0 20px 0;
    }

    /* Metrik kartları için stil */
    div[data-testid="metric-container"] {
        background-color: rgba(28, 131, 225, 0.1);
        border: 1px solid rgba(28, 131, 225, 0.2);
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Metrik başlığı */
    div[data-testid="metric-container"] label {
        font-weight: bold;
        color: #b900f7;
    }

    /* Metrik değeri */
    div[data-testid="metric-container"] div {
        color: #4100b2;
    }

    /* Hikaye bölümleri */
    .story-section {
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 10px;
        background-color: rgba(240, 242, 246, 0.1);
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Veri dosyasını yükle
try:
    preprocessed_data = pd.read_csv("CreditScore.csv")
except Exception as e:
    st.error(f"Veri yüklenirken hata oluştu: {e}")
    preprocessed_data = None

if preprocessed_data is not None:
    # Sidebar filtreleri
    with st.sidebar:
        st.image("logo.png")
        st.subheader("Filtreleme")

        # Kredi skoru filtreleme
        credit_options = preprocessed_data['Credit_Score'].unique().tolist()
        credit_score = st.multiselect("Kredi Skoru", options=credit_options, default=credit_options)

        # Yaş aralığı filtresi
        min_age = int(preprocessed_data["Age"].min())
        max_age = int(preprocessed_data["Age"].max())
        age_range = st.slider("Yaş Aralığı", min_age, max_age, (min_age, max_age))

        # Meslek filtresi
        occupations = preprocessed_data['Occupation'].unique().tolist()
        selected_occupation = st.selectbox("Meslek", ["Tümü"] + occupations)

        # Ay filtresi
        months = preprocessed_data['Month'].unique().tolist()
        selected_month = st.multiselect("Ay", options=months, default=months)

        # Veri özeti
        st.divider()
        st.caption("📊 Veri Özeti")
        st.caption(f"Toplam kayıt: {preprocessed_data.shape[0]}")
        st.caption(f"Toplam özellik: {preprocessed_data.shape[1]}")

    # Filtreleme işlemleri
    filtered_data = preprocessed_data.copy()

    if credit_score:
        filtered_data = filtered_data[filtered_data["Credit_Score"].isin(credit_score)]

    filtered_data = filtered_data[(filtered_data["Age"] >= age_range[0]) &
                                  (filtered_data["Age"] <= age_range[1])]

    if selected_occupation != "Tümü":
        filtered_data = filtered_data[filtered_data['Occupation'] == selected_occupation]

    if selected_month:
        filtered_data = filtered_data[filtered_data["Month"].isin(selected_month)]

    st.info(f"📊 Gösterilen kayıt sayısı: {len(filtered_data)}")

    # İLK BÖLÜM: Müşteri Profili
    st.markdown('<div class="section-header"><h2>📱 Bölüm 1: Müşteri Profili</h2></div>', unsafe_allow_html=True)

    # Genel Metrikleri Göster
    st.subheader("Temel Finansal Göstergeler")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Ortalama Yaş", f"{filtered_data['Age'].mean():.1f}")

    with col2:
        st.metric("Ortalama Gelir", f"${filtered_data['Annual_Income'].mean():,.0f}")

    with col3:
        st.metric("Ortalama Borç", f"${filtered_data['Outstanding_Debt'].mean():,.0f}")

    with col4:
        ratio = (filtered_data['Outstanding_Debt'] / filtered_data['Annual_Income']).mean()
        st.metric("Borç-Gelir Oranı", f"{ratio:.2f}")

    # Yaş dağılımı ve kredi skoru ilişkisi
    st.subheader("Yaş Gruplarına Göre Müşteri Dağılımı")

    # Yaş grubu oluştur
    filtered_data['Yaş Grubu'] = pd.cut(
        filtered_data['Age'],
        bins=[17, 25, 35, 45, 55, 65, 100],
        labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    )

    col1, col2 = st.columns(2)
    with col1:
        # Yaş grubu dağılımı
        age_group_counts = filtered_data['Yaş Grubu'].value_counts().reset_index()
        age_group_counts.columns = ['Yaş Grubu', 'Sayı']
        age_group_counts = age_group_counts.sort_values('Yaş Grubu')

        fig = px.bar(
            age_group_counts,
            x='Yaş Grubu',
            y='Sayı',
            title='Yaş Grubu Dağılımı',
            color='Yaş Grubu',
            color_discrete_sequence=color_palette,
            text_auto=True
        )
        fig.update_layout(template="plotly_dark", yaxis_title="Müşteri Sayısı")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Credit Mix ve Kredi Skoru İlişkisi
        credit_mix_score = filtered_data.groupby(['Credit_Mix', 'Credit_Score']).size().reset_index(name='Count')

        fig = px.bar(
            credit_mix_score,
            x='Credit_Mix',
            y='Count',
            color='Credit_Score',
            title='Kredi Türü Çeşitliliği ve Kredi Skoru',
            color_discrete_sequence=color_palette,
            barmode='group'
        )
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Kredi Türü Çeşitliliği",
            yaxis_title="Müşteri Sayısı"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Meslek dağılımı
    st.subheader("Mesleklere Göre Müşteri Analizi")

    col1, col2 = st.columns(2)
    with col1:
        # Meslek bazında kredi skoru dağılımı
        occupation_score = filtered_data.groupby(['Occupation', 'Credit_Score']).size().reset_index(name='Count')

        fig = px.bar(
            occupation_score,
            x='Occupation',
            y='Count',
            color='Credit_Score',
            title='Mesleklere Göre Kredi Skoru Dağılımı',
            color_discrete_sequence=color_palette,
            barmode='stack'
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Meslek", yaxis_title="Müşteri Sayısı",
                          xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Meslekler ve Kredi Kartı Sayısı
        fig = px.bar(
            filtered_data.groupby('Occupation')['Num_Credit_Card'].mean().reset_index(),
            x='Occupation',
            y='Num_Credit_Card',
            title='Mesleklere Göre Ortalama Kredi Kartı Sayısı',
            color_discrete_sequence=[color_palette[2]],
            text_auto=True
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Meslek", yaxis_title="Ortalama Kredi Kartı Sayısı",
                          xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # İKİNCİ BÖLÜM: Kredi Skoru Dinamiği
    st.markdown('<div class="section-header"><h2>📈 Bölüm 2: Kredi Skoru Dinamiği</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    *Kredi skorunun nasıl dağıldığını ve hangi faktörlerden etkilendiğini inceleyelim. Bu bölümde, kredi skoru
    dağılımları ve kredi karması ilişkileri ele alınmaktadır.*
    """)

    col1, col2 = st.columns(2)
    with col1:
        # Kredi skoru dağılımı
        fig = px.histogram(
            filtered_data,
            x='Credit_Score',
            title='Kredi Skoru Dağılımı',
            color='Credit_Score',
            text_auto=True,
            color_discrete_sequence=color_palette,
            nbins=len(filtered_data['Credit_Score'].unique())
        )
        fig.update_layout(
            template="plotly_dark",
            bargap=0.2,
            xaxis_title="Kredi Skoru",
            yaxis_title="Müşteri Sayısı"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Credit Mix ve Kredi Skoru İlişkisi - Sunburst
        fig = px.sunburst(
            filtered_data,
            path=['Credit_Score', 'Credit_Mix'],
            title='Kredi Skoru ve Kredi Karması Dağılımı',
            color='Credit_Score',
            color_discrete_sequence=color_palette
        )
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), template="plotly_dark")
        fig.update_traces(textinfo='label+percent entry')
        st.plotly_chart(fig, use_container_width=True)

    # Ay bazında kredi skoru
    st.subheader("Zaman İçinde Kredi Skoru Değişimi")

    # Ay bazında kredi skoru dağılımı
    month_score = filtered_data.groupby(['Month', 'Credit_Score']).size().reset_index(name='Count')

    fig = px.bar(
        month_score,
        x='Month',
        y='Count',
        color='Credit_Score',
        title='Aylara Göre Kredi Skoru Dağılımı',
        color_discrete_sequence=color_palette,
        barmode='stack'
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Ay", yaxis_title="Müşteri Sayısı")
    st.plotly_chart(fig, use_container_width=True)

    # Diğer kategorik değişkenler
    col1, col2 = st.columns(2)
    with col1:
        # Kredi Karması ve Kredi Skoru
        credit_mix_score = filtered_data.groupby(['Credit_Mix', 'Credit_Score']).size().reset_index(name='Count')

        fig = px.bar(
            credit_mix_score,
            x='Credit_Mix',
            y='Count',
            color='Credit_Score',
            title='Kredi Karmasına Göre Kredi Skoru Dağılımı',
            color_discrete_sequence=color_palette,
            barmode='stack'
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Kredi Karması", yaxis_title="Müşteri Sayısı")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Ödeme davranışına göre kredi skoru dağılımı
        payment_score = filtered_data.groupby(['Payment_Behaviour', 'Credit_Score']).size().reset_index(name='Count')

        fig = px.bar(
            payment_score,
            x='Payment_Behaviour',
            y='Count',
            color='Credit_Score',
            title='Ödeme Davranışına Göre Kredi Skoru Dağılımı',
            color_discrete_sequence=color_palette,
            barmode='stack'
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Ödeme Davranışı", yaxis_title="Müşteri Sayısı",
                          xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # ÜÇÜNCÜ BÖLÜM: Borç ve Ödeme Analizi
    st.markdown('<div class="section-header"><h2>💰 Bölüm 3: Borç ve Ödeme Analizi</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    *Müşterilerin borç durumları ve ödeme davranışları kredi skorunu nasıl etkiliyor? Bu bölümde, borç seviyeleri ve
    ödeme alışkanlıklarının kredi skoruyla ilişkisi incelenmektedir.*
    """)

    # Minimum ödeme durumu ve kredi skoru
    col1, col2 = st.columns(2)
    with col1:
        # Minimum ödeme durumu ve Kredi Skoru
        min_payment_score = filtered_data.groupby(['Payment_of_Min_Amount', 'Credit_Score']).size().reset_index(
            name='Count')

        fig = px.bar(
            min_payment_score,
            x='Payment_of_Min_Amount',
            y='Count',
            color='Credit_Score',
            title='Minimum Ödeme Durumuna Göre Kredi Skoru',
            color_discrete_sequence=color_palette,
            barmode='stack'
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Minimum Ödeme Durumu", yaxis_title="Müşteri Sayısı")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Kredi Skoruna Göre Borç-Gelir Oranı
        fig = px.box(
            filtered_data,
            x="Credit_Score",
            y="Debt_to_Income_Ratio",
            color="Credit_Score",
            title="Kredi Skoruna Göre Borç-Gelir Oranı",
            color_discrete_sequence=color_palette
        )
        fig.update_layout(template="plotly_dark", yaxis_title="Borç-Gelir Oranı")
        st.plotly_chart(fig, use_container_width=True)

    # Gecikme ve borç ilişkisi
    st.subheader("Gecikmeli Ödemeler ve Borçlar")

    col1, col2 = st.columns(2)
    with col1:
        # Gecikme Günleri Kredi Skoru İlişkisi
        fig = px.box(
            filtered_data,
            x="Credit_Score",
            y="Delay_from_due_date",
            color="Credit_Score",
            title="Kredi Skoruna Göre Gecikme Günleri",
            color_discrete_sequence=color_palette
        )
        fig.update_layout(template="plotly_dark", yaxis_title="Gecikme Günleri")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Gecikme sayısı ve borç ilişkisi
        fig = px.scatter(
            filtered_data,
            x="Num_of_Delayed_Payment",
            y="Outstanding_Debt",
            color="Credit_Score",
            title="Gecikme Sayısı ve Borç İlişkisi",
            color_discrete_sequence=color_palette,
            opacity=0.7,
            size="Annual_Income",
            size_max=15,
            hover_data=["Age", "Occupation"]
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Gecikme Sayısı", yaxis_title="Borç ($)")
        st.plotly_chart(fig, use_container_width=True)

    # Borç-Gelir Oranı Dağılımı
    fig = px.histogram(
        filtered_data,
        x="Debt_to_Income_Ratio",
        color="Credit_Score",
        title="Borç-Gelir Oranı Dağılımı",
        color_discrete_sequence=color_palette,
        barmode="overlay",
        nbins=30
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Borç-Gelir Oranı", yaxis_title="Müşteri Sayısı")
    st.plotly_chart(fig, use_container_width=True)

    # DÖRDÜNCÜ BÖLÜM: Finansal Ürün Kullanımı
    st.markdown('<div class="section-header"><h2>💳 Bölüm 4: Finansal Ürün Kullanımı</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    *Müşterilerin kullandıkları finansal ürünler, finansal davranışlarını ve kredi skorlarını nasıl şekillendiriyor?
    Bu bölümde, kredi kartı kullanımı, kredi türleri ve bunların kredi skoru üzerindeki etkileri incelenmektedir.*
    """)

    # Kredi Kartı ve Banka Hesabı Analizi
    st.subheader("Kredi Kartı ve Banka Hesabı Kullanımı")

    col1, col2 = st.columns(2)
    with col1:
        # Kredi Kartı Sayısı ve Banka Hesabı Sayısı Dağılımı
        card_account_avg = filtered_data.groupby('Credit_Score')[
            ['Num_Credit_Card', 'Num_Bank_Accounts']].mean().reset_index()

        # Veriyi uzun formata dönüştür
        card_account_melt = pd.melt(
            card_account_avg,
            id_vars=['Credit_Score'],
            value_vars=['Num_Credit_Card', 'Num_Bank_Accounts'],
            var_name='Account_Type',
            value_name='Average_Count'
        )

        # Değişken isimlerini Türkçeye çevir
        card_account_melt['Account_Type'] = card_account_melt['Account_Type'].replace({
            'Num_Credit_Card': 'Kredi Kartı Sayısı',
            'Num_Bank_Accounts': 'Banka Hesabı Sayısı'
        })

        fig = px.bar(
            card_account_melt,
            x='Credit_Score',
            y='Average_Count',
            color='Account_Type',
            title='Kredi Skoruna Göre Ortalama Kredi Kartı ve Banka Hesabı Sayısı',
            color_discrete_sequence=color_palette,
            barmode='group'
        )
        fig.update_layout(template="plotly_dark", yaxis_title="Ortalama Sayı")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Aylık Bakiye Dağılımı
        fig = px.violin(
            filtered_data,
            x="Credit_Score",
            y="Monthly_Balance",
            color="Credit_Score",
            box=True,
            title="Kredi Skoruna Göre Aylık Bakiye",
            color_discrete_sequence=color_palette
        )
        fig.update_layout(template="plotly_dark", yaxis_title="Aylık Bakiye ($)")
        st.plotly_chart(fig, use_container_width=True)

    # Kredi Tipleri Analizi
    st.subheader("Kredi Tipleri ve Kullanım Analizi")

    # Kredi tiplerini içeren sütunlar
    loan_types = ["Auto Loan", "Credit-Builder Loan", "Debt Consolidation Loan",
                  "Home Equity Loan", "Mortgage Loan", "Not Specified",
                  "Payday Loan", "Personal Loan", "Student Loan"]

    # Kredi tiplerinin dağılımını hesapla
    loan_counts = []
    for loan_type in loan_types:
        loan_counts.append({
            'Kredi Tipi': loan_type,
            'Sayı': filtered_data[loan_type].sum()
        })

    loan_df = pd.DataFrame(loan_counts)

    # Kredi tipleri dağılımı - ana bar chart
    fig = px.bar(
        loan_df,
        x='Kredi Tipi',
        y='Sayı',
        title='Kredi Tipleri Dağılımı',
        color='Kredi Tipi',
        color_discrete_sequence=px.colors.sequential.Cividis,
        text_auto=True
    )
    fig.update_layout(template="plotly_dark", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Her kredi tipinin kullanım oranını hesapla
        loan_usage = pd.DataFrame()

        for loan_type in loan_types:
            # Her bir kredi türü için kullanım sayılarını al
            loan_users_by_score = filtered_data.groupby('Credit_Score')[loan_type].sum().reset_index()
            loan_users_by_score.rename(columns={loan_type: 'Count'}, inplace=True)
            loan_users_by_score['Loan_Type'] = loan_type

            # Toplam data frame'e ekle
            loan_usage = pd.concat([loan_usage, loan_users_by_score])

        # Grafik oluştur
        fig = px.bar(
            loan_usage,
            x='Loan_Type',
            y='Count',
            color='Credit_Score',
            title='Kredi Tipine Göre Kredi Skoru Dağılımı',
            color_discrete_sequence=color_palette,
            barmode='group'
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Kredi Tipi", yaxis_title="Kullanıcı Sayısı",
                          xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Her kredi tipi için ortalama kredi kartı ve banka hesabı sayısı
        account_by_loan = pd.DataFrame()

        for loan_type in loan_types:
            # Her bir kredi türünü kullananların ortalama hesap sayıları
            loan_users = filtered_data[filtered_data[loan_type] == 1]

            if not loan_users.empty:
                avg_accounts = {
                    'Loan_Type': loan_type,
                    'Avg_Credit_Cards': loan_users['Num_Credit_Card'].mean(),
                    'Avg_Bank_Accounts': loan_users['Num_Bank_Accounts'].mean()
                }

                account_by_loan = pd.concat([account_by_loan, pd.DataFrame([avg_accounts])])

        # Veriyi uzun formata dönüştür
        account_melt = pd.melt(
            account_by_loan,
            id_vars=['Loan_Type'],
            value_vars=['Avg_Credit_Cards', 'Avg_Bank_Accounts'],
            var_name='Account_Type',
            value_name='Average'
        )

        # Değişken isimlerini Türkçeye çevir
        account_melt['Account_Type'] = account_melt['Account_Type'].replace({
            'Avg_Credit_Cards': 'Ortalama Kredi Kartı Sayısı',
            'Avg_Bank_Accounts': 'Ortalama Banka Hesabı Sayısı'
        })

        # Grafik oluştur
        fig = px.bar(
            account_melt,
            x='Loan_Type',
            y='Average',
            color='Account_Type',
            title='Kredi Tipine Göre Ortalama Hesap Sayıları',
            color_discrete_sequence=[color_palette[1], color_palette[4]],
            barmode='group'
        )
        fig.update_layout(template="plotly_dark", xaxis_title="Kredi Tipi", yaxis_title="Ortalama Sayı",
                          xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # BEŞİNCİ BÖLÜM: Faktörler Arası İlişkiler
    st.markdown('<div class="section-header"><h2>🔗 Bölüm 5: Faktörler Arası İlişkiler</h2></div>',
                unsafe_allow_html=True)
    st.markdown("""
    *Finansal faktörler birbirleriyle nasıl ilişkilidir? Bu bölümde, kredi skorunu etkileyen faktörlerin 
    korelasyonları ve birbirleriyle olan ilişkileri incelenmektedir.*
    """)

    # Donut Chart - Kredi Skoru & Kredi Mix
    st.subheader("Kredi Skoru ve Kredi Karması İlişkisi")

    # Donut Chart için veri hazırlama
    donut_data = filtered_data.groupby(['Credit_Score', 'Credit_Mix']).size().reset_index(name='Count')
    donut_data['Percentage'] = donut_data['Count'] / donut_data['Count'].sum() * 100
    donut_data['Label'] = donut_data['Credit_Score'] + ' - ' + donut_data['Credit_Mix']

    # Donut Chart
    fig = px.pie(
        donut_data,
        names='Label',
        values='Percentage',
        title='Kredi Skoru ve Kredi Karması Dağılımı',
        color='Credit_Score',
        color_discrete_sequence=color_palette,
        hole=0.03
    )
    fig.update_traces(
        texttemplate='%{label}<br>%{percent}',
        textposition='inside',
        textfont=dict(size=14, family="Arial", color="white", weight="bold")  # Yazılar daha büyük ve kalın
    )
    # Genel görünüm ayarları
    fig.update_layout(
        template="plotly_dark",
        width=1900,  # genislik
        height=1200,  # yükseklik
        font=dict(size=14, family="Arial", color="white")  # Genel yazı fontu
    )
    st.plotly_chart(fig, use_container_width=True)

    # Korelasyon Matrisi
    st.subheader("Faktörler Arası Korelasyon Analizi")

    # Önemli sayısal değişkenlerin seçimi
    important_cols = [
        'Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Outstanding_Debt',
        'Num_Credit_Card', 'Num_Bank_Accounts', 'Credit_Utilization_Ratio',
        'Debt_to_Income_Ratio', 'Delay_from_due_date', 'Num_of_Delayed_Payment',
        'Monthly_Balance', 'Total_EMI_per_month', 'Total_Monthly_Expenses',
        'Credit_History_Age', 'Num_Credit_Inquiries', "Auto Loan", "Credit-Builder Loan", "Debt Consolidation Loan",
        "Home Equity Loan", "Mortgage Loan", "Not Specified",
        "Payday Loan", "Personal Loan", "Student Loan"
    ]

    # Mevcut sütunları kontrol et
    numeric_features = filtered_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    selected_cols = [col for col in important_cols if col in numeric_features]

    # Korelasyon matrisinin hesaplanması ve yuvarlanması
    corr_matrix = filtered_data[selected_cols].corr().round(2)

    # Plotly ile korelasyon matrisi görselleştirmesi
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="GnBu",
        title='Değişkenler Arası Korelasyon Matrisi',
        labels=dict(color="Korelasyon")
    )

    # Grafik boyut ayarları
    fig.update_layout(
        height=60 * len(selected_cols),  # Her değişken için 60 yükseklik
        width=120 * len(selected_cols),  # Her değişken için 120px genişlik
        template="plotly_dark"
    )

    # Grafiğin Streamlit üzerinde gösterilmesi
    st.plotly_chart(fig, use_container_width=True)

    # En Güçlü Korelasyonların Tablosu
    st.subheader("En Güçlü Korelasyonlar")

    # Üçgen matrisin açılması ve sıralanması
    corr_pairs = corr_matrix.unstack().sort_values(ascending=False)

    # Kendisiyle olan korelasyonlar (1.0) kaldırılır
    corr_pairs = corr_pairs[corr_pairs < 0.99]

    # Güçlü korelasyonların (|r| > 0.3) filtrelenmesi
    strong_corr = corr_pairs[abs(corr_pairs) > 0.3]

    # Sonuç varsa tablo olarak gösterilir
    if not strong_corr.empty:
        strong_corr_df = pd.DataFrame(strong_corr).reset_index()
        strong_corr_df.columns = ['Değişken 1', 'Değişken 2', 'Korelasyon']

        # Korelasyon tablosunun Streamlit üzerinde gösterimi
        styled_df = strong_corr_df.style \
            .background_gradient(cmap='Blues', subset=['Korelasyon']) \
            .set_properties(**{
            'text-align': 'center',
            'font-weight': 'bold',
            'border': '1px solid #ccc',
            'padding': '5px'
        }) \
            .format({'Korelasyon': '{:.2f}'}) \
            .set_table_styles([
            {'selector': 'th', 'props': [('font-size', '16px'), ('background-color', '#84bc98'), ('color', 'white'),
                                         ('text-align', 'center')]}
        ])

        # Streamlit tablosu
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=560)
    else:
        st.info("Belirtilen eşik değerine göre güçlü bir korelasyon bulunmamaktadır.")

    # SONUÇ BÖLÜMÜ
    st.markdown('<div class="section-header"><h2>🏁 Kredi Skor Analiz Sonucu</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    *Kredi skorunun arkasındaki hikayeyi birlikte keşfettik. Bu dashboard sayesinde:*

    1. **Müşteri Profillerini** daha iyi anlayarak hedef kitleyi tanıdık.
    2. **Kredi Skoru Dinamiklerini** görerek hangi faktörlerin etkili olduğunu gördük.
    3. **Borç ve Ödeme Davranışlarının** kredi skoruna etkisini inceleyebildik.
    4. **Finansal Ürün Kullanımı** ile kredi skoru arasındaki ilişkileri keşfettik.
    5. **Faktörler Arası İlişkileri** analiz ederek daha derin içgörüler elde ettik.
    """)

    # Kredi skoru dağılımı - Pasta grafik
    fig = px.pie(
        filtered_data,
        names='Credit_Score',
        title='Kredi Skoru Dağılımı Özeti',
        color='Credit_Score',
        color_discrete_sequence=color_palette,
        hole=0.2  # Donut efekti istersen
    )
    fig.update_traces(
        textinfo='percent+label',
        textfont_size=16,  # İç yazı fontu
        pull=[0.05] * len(filtered_data['Credit_Score'].unique())  # Dilimleri hafifçe çek
    )
    fig.update_layout(
        template="plotly_dark",
        width=800,  # Grafik genişliği
        height=600,  # Grafik yüksekliği
        title_font_size=16,
        legend=dict(
            font=dict(size=16),  # Sağdaki yazılar (legend)
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02  # Sağ tarafa yasla
        ),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    st.plotly_chart(fig, use_container_width=False)

    # Ödeme davranışı özeti - Pasta grafik
    payment_counts = filtered_data['Payment_Behaviour'].value_counts().reset_index()
    payment_counts.columns = ['Ödeme Davranışı', 'Sayı']

    fig = px.pie(
        payment_counts,
        names='Ödeme Davranışı',
        values='Sayı',
        title='Ödeme Davranışı Özeti',
        color_discrete_sequence=color_palette,
        hole=0.1
    )

    fig.update_traces(
        textinfo='percent+label',
        textfont_size=18,  # Dilim üzerindeki yazılar
        pull=[0.03] * len(payment_counts)  # Dilimleri biraz daha dışarı çek
    )

    fig.update_layout(
        template="plotly_dark",
        width=1800,  # Daha büyük grafik
        height=1000,  # Daha uzun grafik
        legend=dict(
            font=dict(size=18),
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=2.50  # Legend'ı grafikten daha uzağa koy
        ),
        margin=dict(t=80, b=60, l=60, r=100)  # Sağ boşluk artırıldı
    )

    st.plotly_chart(fig, use_container_width=False)

    # Borç-gelir oranı gruplandırması - Bar grafik

    filtered_data['Borç-Gelir Grubu'] = pd.cut(
        filtered_data['Debt_to_Income_Ratio'],
        bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 10],
        labels=['0-0.1', '0.1-0.2', '0.2-0.3', '0.3-0.4', '0.4-0.5', '0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0+']
    )

    debt_income_counts = filtered_data['Borç-Gelir Grubu'].value_counts().reset_index()
    debt_income_counts.columns = ['Borç-Gelir Grubu', 'Sayı']

    fig = px.bar(
        debt_income_counts,
        x='Borç-Gelir Grubu',
        y='Sayı',
        title='Borç-Gelir Oranı Dağılımı Özeti',
        color='Borç-Gelir Grubu',
        color_discrete_sequence=color_palette,
        text_auto=True
    )
    fig.update_layout(template="plotly_dark", width=1900, height=600, xaxis_title="Borç-Gelir Grubu",
                      yaxis_title="Müşteri Sayısı")
    st.plotly_chart(fig, use_container_width=True)

    # Dashboard sonucu
    st.success("""
    📌 **Temel Bulgular**

    * Yüksek kredi skoruna sahip müşteriler genellikle daha düşük borç-gelir oranına sahiptir.
    * Ödeme davranışları, kredi skoru üzerinde güçlü bir etkiye sahiptir.
    * Düzenli minimum ödeme yapan müşterilerin kredi skorları daha yüksektir.
    * Kredi kartı ve banka hesabı kullanım sayıları ile kredi skoru arasında pozitif bir ilişki vardır.
    * Meslek grupları arasında finansal davranışlar ve kredi skorları farklılık göstermektedir.

    Bu içgörüler, müşteri deneyimini iyileştirmek ve daha hedefli finansal hizmetler sunmak için kullanılabilir.
    """)

    # Footer
    st.markdown("---")