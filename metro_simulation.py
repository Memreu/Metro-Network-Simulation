from collections import defaultdict, deque
# defaultdict: Varsayılan değer atanmış sözlükler oluşturur.
# deque: Çift yönlü veri yapısı 
import heapq
# heapq: Min-heap için yığın işlemleri (en küçük elemanı öne alır).
from typing import Dict, List, Tuple, Optional
# Dict: Sözlük 
# List: Liste 
# Tuple: Sabit uzunluklu veri
# Optional: Olabilecek ya da olmayacak değerler


class Istasyon:                                                                
    """
    Metro istasyonunu temsil eden sınıftır.
    
    Açıklama:
        idx (str): İstasyonun kimliği
        ad (str): İstasyonun isimi
        hat (str): İstasyonun bulunduğu metro hattı
        komsular (List[Tuple['Istasyon', int]]): Metro hattımıza komşu istasyonlar ve yol süreleri
        
        Olası Hata Sebep : Bilgi doldurmaktan kaçınan kullanıcı.
    """
    def __init__(self, idx: str, ad: str, hat: str):
        if not idx or not ad or not hat:
            raise ValueError("İstasyon bilgileri mutlaka doldurulmalıdır.")
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, Istasyon: 'Istasyon', sure: int) -> None:
         """
         Komşu istasyon eklemeye yarayan fonksiyondur.
         
         Açıklama:
         istasyon (Istasyon): Ekleyeceğimiz komşu istasyon
         sure (int): İki istasyon arasındaki yolda dakika biçiminde geçirilecek süre
                 
         Olası Hata Sebep : İki istasyon arası süreyi negatif giren kullanıcı.
         """
         if sure < 0:
             raise ValueError("İki istasyon arası süre negatif değer alamaz.")
         self.komsular.append((Istasyon, sure))

class MetroAgi:
    """
    Bu sınıf en kısa ve en hızlı rotaları bulmamız için değerlidir.
    """
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """
        Fonksiyon sayesinde yeni bir istasyon ekleriz.
        Class istasyon kısmındaki anahtar kelimeler ile aynı anahtar kelimelere sahibiz ekstra açıklama yapmıyorum.
        """
        if not idx or not ad or not hat:
            raise ValueError("İstasyon bilgileri boş bırakılamaz")
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """
        İki istasyon arasına bağlantı eklememizi sağlar.
        Açıklama:
            istasyon1_id (str): Birinci istasyonun idsi
            istasyon2_id (str): İkinci istasyonun idsi
            sure (int): İki istasyon arasındaki yolda dakika biçiminde geçirilecek süre
            
            Olası Hata Sebep : İki istasyon arası süreyi negatif giren kullanıcı & 
            Yanlış/Eksik istasyon idsi giren kullanıcı & İstasyon idsini boş bırakan kullanıcı
        """
        if sure < 0:        
            raise ValueError("İki istasyon arası süre negatif değer alamaz.")
        if istasyon1_id not in self.istasyonlar or istasyon2_id not in self.istasyonlar:
            raise KeyError("Böyle bir istasyon bulunmuyor.")
        
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """
        BFS kullanarak en az aktarmalı rotayı bulur. BFS kullanma sebebimiz BFS, 
        bir başlangıç düğümünden başlayarak önce yakın düğümleri, 
        ardından bir sonraki seviyedeki düğümleri keşfeder.
        
        Açıklama:
            baslangic_id (str): Başlangıç istasyonunun idsi
            hedef_id (str): Hedef istasyonunun idsi
             
        Raises:
            Olası Hata Sebep : İstasyon idsini hatalı giren kullanıcı
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            raise KeyError("İstasyon mevcut değil")
            
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        hedef #Spyder hedefi yazdın ama hiç kullanmadın hatası verdiği için hatayı kaldırmak amaçlı boş bir satır.
        
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = {baslangic}
        
        while kuyruk:
            mevcut_istasyon, mevcut_rota = kuyruk.popleft()
            
            if mevcut_istasyon.idx == hedef_id:
                return mevcut_rota
                
            for komsu_istasyon, _ in mevcut_istasyon.komsular:
                if komsu_istasyon not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu_istasyon)
                    yeni_rota = mevcut_rota + [komsu_istasyon]
                    kuyruk.append((komsu_istasyon, yeni_rota))
                    
        return None

    def heuristic(self, istasyon: Istasyon, hedef: Istasyon) -> int:
        """
        Alttaki işlem için lazım
        """
        return 1  

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """
        A* algoritması kullandık.En kısa ve en hızlı rotayı etkin bir şekilde bulmak için 
        bir yol arama algoritmasına ihtiyaç duyuyorduk bu ihtiyacı A* kapattı.
        
        Açıklama:
            baslangic_id (str): Başlangıç istasyonuna ait id
            hedef_id (str): Hedef istasyona ait id
            
        Hata Sebep:
            Olası Hata Sebep : İstasyon idsini hatalı giren kullanıcı
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            raise KeyError("İstasyon bulunamadı")

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        
        kuyruk = [(0 + self.heuristic(baslangic, hedef), id(baslangic), baslangic, [baslangic], 0)]
        
        while kuyruk:
            _, _, mevcut_istasyon, mevcut_rota, toplam_sure = heapq.heappop(kuyruk)
            
            if mevcut_istasyon.idx == hedef_id:
                return (mevcut_rota, toplam_sure)
                
            if mevcut_istasyon in ziyaret_edildi:
                continue
                
            ziyaret_edildi.add(mevcut_istasyon)
            
            for komsu_istasyon, sure in mevcut_istasyon.komsular:
                if komsu_istasyon not in ziyaret_edildi:
                    yeni_sure = toplam_sure + sure
                    yeni_rota = mevcut_rota + [komsu_istasyon]
                    
                    heapq.heappush(kuyruk, (yeni_sure + self.heuristic(komsu_istasyon, hedef), 
                                      id(komsu_istasyon), komsu_istasyon, yeni_rota, yeni_sure))
                    
        return None

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 
        

