

🧠 **Credit Score Classification Project**

Bu proje, bireylerin finansal geçmişi ve ödeme davranışlarına dayalı olarak kredi skorlarını sınıflandırmak amacıyla geliştirilmiştir. Klasik gözetimli yöntemlerden başlayarak yarı-gözetimli (pseudo-labeling) modellemeye geçilmiş, sonuçlar karşılaştırmalı olarak değerlendirilmiştir.

---

📁 **Proje Yapısı**

* **data/**
  Temizlenmiş, dönüştürülmüş ve etiketlenmiş veri setlerini içerir.

* **models/**
  Eğitimli modeller (.pkl) burada tutulur. Büyük dosyalar Git LFS ile izlenmektedir.

* **notebooks/**
  Veri ön işleme, modelleme ve deneysel analizlerin yapıldığı Jupyter defterlerini içerir.

* **pages/**
  Streamlit çok sayfalı arayüz yapısı: veri seti açıklamaları ve iki farklı model sayfası.

* **Home.py**
  Streamlit giriş sayfası.

* **logo.png**
  Uygulama logosu.

---

🚀 **Nasıl Kullanılır**

1. Gerekli Python kütüphanelerini kurun (örneğin: requirements.txt dosyasından).
2. Ana sayfayı çalıştırın:

streamlit run Home.py

Uygulama, kredi skorunu tahmin eden modellerin görselleştirilmiş çıktıları ile çalışır.

---

🧪 **Uygulanan Yöntemler**

* SMOTE ile sınıf dengesi denemesi
* Feature engineering ve leakage kontrolü
* PCA ile leaky feature sıkıştırma
* DBSCAN + UMAP ile cluster tabanlı etiketleme
* RandomForest ve Stacking ile klasik modelleme
* Pseudo-label ile yeniden etiketleme ve yarı-gözetimli öğrenme
* Threshold tuning ile karar performansını iyileştirme

---

📊 **Model Karşılaştırması (F1 – Class 1)**

* Üç sınıflı klasik model: 0.80
* İki sınıfa indirgenmiş model: 0.81
* Pseudo-label model: 0.99

---

🧠 **Ne Öğrendik?**

* Etiketler güvenilir değilse klasik modeller zayıf kalır.
* SHAP ve UMAP ile sınıf yapısı analiz edilmeli.
* Pseudo-labeling, dengesiz ve belirsiz sınıflarda büyük avantaj sağlar.
* Basit model + doğru temsil = en sağlam sonuç.

---

📌 **Notlar**

* `models/` klasöründeki `.pkl` dosyaları Git LFS ile yüklenmiştir.
* LSTM, TabNet, zaman serisi gibi yöntemler denenmiş fakat performans katkısı sağlamadığı için proje dışına çıkarılmıştır.

---

📫 **İletişim**

Görüş, öneri ve katkılarınız için:
github.com/ilkerkadirakan
