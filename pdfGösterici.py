import poppler
import tkinter as tk
import mtranslate
import pyperclip
import sys

def işle(yazı):
	işlenecekSöz = ""
	yeniYazı = ""
	#satırbaşından kurtul
	düzenlenmişSözcük =""
	# tüm kelimeleri al ve transtalte için hazırla
	#\n e göre parçala, kelimelerdeki noktalamaları sil ve bilinen sözcük değilse işlnecekler arasına ekle
	for sözcük in " ".join(yazı.split("\n")).split(" "):
		düzenlenmişSözcük = sözcük
		for i in [".",",",":",";","?"]:
			düzenlenmişSözcük = düzenlenmişSözcük.replace(i,"")
		if sözcük != "" and sözcük !="\n" and düzenlenmişSözcük.lower() not in bilinenSözcükler :
			işlenecekSöz += düzenlenmişSözcük + "\n"
	
	#çeviriyi yap, her kelime arası \n var
	#internet yoksa except, siteye ulaşamıyorsa "" döner
	try:
		işlenmisSöz = mtranslate.translate(işlenecekSöz,"tr","en")
	except:
		return yazı,[0]
	if işlenmisSöz == "":
		return yazı,[0]

	ingilizceİlkKonum = 0
	türkçeSonKonum = 0
	sözcükSayısı = 0
	etkinSatır = 1
	çeviriSatırlari=[]
	#her bir satır için ve o satırdaki her sözcük için
	#noktalamalardan arındırıp bilinen sözcüklerde yoksa konumunu bul
	#türkçe ve ingilizce metni doğru uzunlukta olmak için ayarla
	#türkçe ve ingilizceyi alt alta kaydet
	for satır in yazı.split("\n"):
		for sözcük in satır.split(" "):
			düzenlenmişSözcük = sözcük
			for i in  [".",",",":",";","?"]:
				düzenlenmişSözcük = düzenlenmişSözcük.replace(i,"")
			if sözcük != "" and sözcük !="\n" and sözcük !="\x0c" and düzenlenmişSözcük.lower() not in bilinenSözcükler :
				ingilizceİlkKonum = satır.find(sözcük,ingilizceİlkKonum)

				if (ingilizceİlkKonum - türkçeSonKonum) <= 0:
					satır = satır[:ingilizceİlkKonum]+(" "*((türkçeSonKonum - ingilizceİlkKonum) + 1)) + satır[ingilizceİlkKonum:]
					ingilizceİlkKonum = türkçeSonKonum +1

				yeniYazı += (ingilizceİlkKonum - türkçeSonKonum) * " " + işlenmisSöz.split("\n")[sözcükSayısı]
				türkçeSonKonum = ingilizceİlkKonum + len(işlenmisSöz.split("\n")[sözcükSayısı])
				ingilizceİlkKonum += len(sözcük) 
				sözcükSayısı += 1
		ingilizceİlkKonum = 0
		türkçeSonKonum = 0
		yeniYazı += "\n" + satır + "\n"
		çeviriSatırlari.append(etkinSatır)
		etkinSatır += 2 
	
	return yeniYazı, çeviriSatırlari
	

def düzenle(yazı):
	#paragraf koruma
	yazı = "&%+/^!".join(yazı.split("\n\n"))

	c=yazı.split("does, and the only way to have this freedom is to know what your computer is")

	#sonu -\n ile biityorsa kelimeyi tam olarak ekle ve öyle aşağı in
	while (konum := yazı.find("-\n")) != -1:
		if yazı[konum-1] == " ":
			yazı = yazı[:konum-1]+yazı[konum:]
		yazı = yazı[:konum+3].replace('-\n', '',1) + yazı[konum+3:]
		yazı =yazı[:konum] + yazı[konum:].replace(' ', '\n',1)

	#korunan paraf bölgesini geri getir
	yazı = "\n\n".join(yazı.split("&%+/^!"))
	return yazı
	

def basıldığında(düğme):
	global betNumarası
	try:
		if düğme =="Right"or düğme == "Down":
			if betNumarası < toplamBetSayısı - 1:
				betNumarası +=1
		elif düğme == "Left" or düğme == "Up":
			if betNumarası != 0:
				betNumarası -=1
		elif düğme == "Control-c":
			seçilmişYazı = yazıArayüzü.selection_get()
			pyperclip.copy(seçilmişYazı)
		else:
			return

		bet = pdfDosyası.create_page(betNumarası)
		yazı = bet.text()
		yazı = düzenle(yazı)
		yazı, çeviriSatırlari= işle(yazı)
		w=arayüz.winfo_width()
		#yazıArayüzü.configure(font=(yazıTipi,int(w/100 + 2)))
		yazıArayüzü.config(state=tk.NORMAL)
		yazıArayüzü.delete("1.0", tk.END)
		yazıArayüzü.insert(index=tk.END,chars=yazı)
		yazıArayüzü.pack()
		for i in çeviriSatırlari:
			ilk = str(i)+".0"
			son = str(i)+".end"
			yazıArayüzü.tag_add("tr",ilk,son)
		yazıArayüzü.tag_config("tr", background="black", foreground="grey",selectbackground="yellow") 
		yazıArayüzü.config(state=tk.DISABLED)
	   
	except Exception as e:
		print(e)
		pass

if len(sys.argv) < 2:
	print("dosya adı girin")
	exit()

betNumarası=0
yazıTipi = "droid sans mono"
genişlik = 630
yükseklik = 891

#F5F5F5 whitesmoke rengi gayet güzel

dosya = open('./sözcükler',"r")
dosya.seek(0)
bilinenSözcükler  = dosya.read().splitlines()

#arayüz oluştur
arayüz = tk.Tk()
arayüz.geometry(str(genişlik)+'x'+str(yükseklik))
yazıArayüzü = tk.Text(arayüz,height = yükseklik,width=genişlik,font =(yazıTipi, 8) ,bg="black",fg="yellow", inactiveselectbackground="yellow")


#pdf i aç
dosyaAdı = sys.argv[1]
pdfDosyası = poppler.load_from_file(dosyaAdı)
toplamBetSayısı = pdfDosyası.pages
bet = pdfDosyası.create_page(betNumarası)
#yazı al
yazı = bet.text()
yazı = düzenle(yazı)
yazı, çeviriSatırlari= işle(yazı)

yazıArayüzü.config(state=tk.NORMAL)
yazıArayüzü.insert(index=tk.END,chars=yazı)
yazıArayüzü.pack()
for i in çeviriSatırlari:
	ilk = str(i)+".0"
	son = str(i)+".end"
	yazıArayüzü.tag_add("tr",ilk,son)
yazıArayüzü.tag_config("tr", background="black", foreground="grey",selectbackground="yellow") 
yazıArayüzü.config(state=tk.DISABLED)


arayüz.bind("<Left>", lambda x: basıldığında("Left"))
arayüz.bind("<Right>", lambda x: basıldığında("Right"))
arayüz.bind("<Up>", lambda x: basıldığında("Up"))
arayüz.bind("<Down>", lambda x: basıldığında("Down"))
arayüz.bind("<Control-c>", lambda x: basıldığında("Control-c"))
arayüz.mainloop()