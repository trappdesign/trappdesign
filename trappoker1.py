import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class MyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Card App")

        # Ambil path folder gambar, deteksi apakah dari PyInstaller bundling atau tidak
        self.image_folder = self.resource_path('cards_images')
        self.show_card('2_of_clubs.png','2_of_hearts.png','2_of_diamonds.png','2_of_spades.png','3_of_clubs.png','3_of_hearts.png','3_of_diamonds.png','3_of_spades.png','4_of_clubs.png','4_of_hearts.png','4_of_diamonds.png','4_of_spades.png','5_of_clubs.png','5_of_hearts.png','5_of_diamonds.png','5_of_spades.png','6_of_clubs.png','6_of_hearts.png','6_of_diamonds.png','6_of_spades.png','7_of_clubs.png','7_of_hearts.png','7_of_diamonds.png','7_of_spades.png','8_of_clubs.png','8_of_hearts.png','8_of_diamonds.png','8_of_spades.png','9_of_clubs.png','9_of_hearts.png','9_of_diamonds.png','9_of_spades.png','10_of_clubs.png','10_of_hearts.png','10_of_diamonds.png','10_of_spades.png','10_of_clubs.png','10_of_hearts.png','10_of_diamonds.png','10_of_spades.png','10_of_clubs.png','10_of_hearts.png','10_of_diamonds.png','10_of_spades.png')
        self.show_card('j_of_clubs.png','j_of_hearts.png','j_of_diamonds.png','j_of_spades.png','k_of_clubs.png','k_of_hearts.png','k_of_diamonds.png','k_of_spades.png','q_of_clubs.png','q_of_hearts.png','q_of_diamonds.png','q_of_spades.png','back_png')


    def resource_path(self, relative_path):
        """ Dapatkan path absolut (handle _MEIPASS kalau dibundle dengan PyInstaller) """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def show_card(self, image_name):
        # Path lengkap ke gambar di folder cards_images
        image_path = os.path.join(self.image_folder, image_name)

        # Load gambar (pakai PIL)
        img = Image.open(image_path)
        img = img.resize((200, 300))  # Contoh resize
        self.card_image = ImageTk.PhotoImage(img)

        # Tampilkan gambar di label
        label = tk.Label(self.master, image=self.card_image)
        label.pack()


# Kelas untuk kartu
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()

    def get_value(self):
        """Menentukan nilai kartu untuk perhitungan permainan"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_image(self):
        """Mendapatkan gambar kartu sesuai suit dan rank"""
        image_path = f"cards_images/{self.rank}_of_{self.suit}.png"
        return image_path

# Kelas untuk deck kartu
class Deck:
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

# Menentukan kombinasi kartu (Pair, Two Pair, Flush, Straight)
def check_hand(hand):
    values = [card.rank for card in hand]
    suits = [card.suit for card in hand]
    
    # Check for Flush (semua kartu dengan suit yang sama)
    if len(set(suits)) == 1:
        return "Flush"

    # Check for Pair, Two Pair, Straight
    value_counts = {value: values.count(value) for value in values}
    pairs = [value for value, count in value_counts.items() if count == 2]
    three_of_a_kind = [value for value, count in value_counts.items() if count == 3]
    four_of_a_kind = [value for value, count in value_counts.items() if count == 4]

    # Check for Pair
    if len(pairs) == 1:
        return "Pair"
    
    # Check for Two Pair
    if len(pairs) == 2:
        return "Two Pair"
    
    # Check for Straight
    sorted_values = sorted([card.value for card in hand])
    if sorted_values == list(range(sorted_values[0], sorted_values[0] + len(sorted_values))):
        return "Straight"

    # Jika tidak ada kombinasi lainnya
    return "High Card"

# Fungsi untuk memulai permainan
def start_game():
    global player_coins, bet_amount, round_count, pot

    if bet_amount <= 0:
        result_label.config(text="Please place a valid bet!")
        return

    # Mengurangi koin berdasarkan taruhan
    player_coins -= bet_amount
    pot += bet_amount
    player_coin_label.config(text=f"Your coins: {player_coins}")
    pot_label.config(text=f"Pot: {pot}")

    deck = Deck()
    player_hand = [deck.draw(), deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw(), deck.draw()]

    # Update tampilan GUI
    player_label.config(text=f"Your hand: {', '.join(str(card) for card in player_hand)}")
    dealer_label.config(text=f"Dealer's hand: {', '.join(str(card) for card in dealer_hand)}")

    # Tampilkan gambar kartu
    display_hand(player_hand, player_canvas)
    display_hand(dealer_hand, dealer_canvas)

    # Periksa siapa yang menang
    player_combination = check_hand(player_hand)
    dealer_combination = check_hand(dealer_hand)

    result_label.config(text=f"Player has: {player_combination}, Dealer has: {dealer_combination}")
    
    if player_combination == dealer_combination:
        result_label.config(text="It's a tie!")
        player_coins += bet_amount  # Pemain mendapatkan kembali taruhannya jika seri
    elif player_combination > dealer_combination:
        result_label.config(text="You Win!")
        player_coins += pot  # Pemain mendapatkan seluruh pot
    else:
        result_label.config(text="Dealer Wins!")
        pot = 0  # Reset pot jika dealer menang

    # Update saldo koin pemain
    player_coin_label.config(text=f"Your coins: {player_coins}")
    round_count += 1  # Menambah ronde
    bet_amount_label.config(text=f"Bet for round {round_count}: {bet_amount}")

def display_hand(hand, canvas):
    """Menampilkan gambar kartu pada canvas"""
    for widget in canvas.winfo_children():
        widget.destroy()  # Hapus gambar sebelumnya

    for index, card in enumerate(hand):
        image_path = card.get_image()
        try:
            image = Image.open(image_path)
            image = image.resize((100, 150))  # Ubah ukuran gambar agar sesuai
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(canvas, image=photo)
            label.image = photo  # Simpan referensi gambar
            label.grid(row=0, column=index, padx=5)
        except Exception as e:
            print(f"Error loading image for {card}: {e}")

# Fungsi untuk menempatkan taruhan
def place_bet():
    global player_coins, bet_amount
    try:
        bet_amount = int(bet_entry.get())  # Indentasi konsisten (4 spasi)
        if bet_amount > player_coins:
            result_label.config(text="You don't have enough coins!")
        elif bet_amount <= 0:
            result_label.config(text="Please enter a valid bet amount!")
        else:
            result_label.config(text=f"Bet placed: {bet_amount} coins")
            bet_amount_label.config(text=f"Bet for round 1: {bet_amount} coins")
    except ValueError:
        result_label.config(text="Please enter a valid number for the bet!")
# Fungsi untuk fold
def fold():
    global bet_amount
    bet_amount = 0
    result_label.config(text="You folded!")
    bet_amount_label.config(text="Bet: 0 coins")

# Fungsi untuk raise (menaikkan taruhan)
def raise_bet():
    global bet_amount, player_coins, pot
    try:
        raise_value = int(raise_entry.get())  # Ambil nilai raise dari input
        if raise_value > player_coins:
            result_label.config(text="You don't have enough coins for this raise!")
        elif raise_value <= 0:
            result_label.config(text="Please enter a valid raise amount!")
        else:
            bet_amount += raise_value  # Tambahkan nilai raise ke taruhan
            player_coins -= raise_value  # Kurangi koin pemain
            pot += raise_value  # Tambahkan ke pot
            result_label.config(text=f"Bet raised by {raise_value} coins!")
            bet_amount_label.config(text=f"New bet: {bet_amount} coins")
            player_coin_label.config(text=f"Your coins: {player_coins}")
            pot_label.config(text=f"Pot: {pot} coins")
    except ValueError:
        result_label.config(text="Please enter a valid number to raise.")

# Fungsi untuk call (memanggil taruhan)
def call():
    global player_coins, bet_amount, pot 
    player_coins -= bet_amount
    pot += bet_amount
    player_coin_label.config(text=f"Your coins: {player_coins}")
    result_label.config(text="You called the bet!")


# Membuat GUI
root = tk.Tk()
root.title("trapp'oker")
root.configure(background="green")
root.geometry("800x650")
root.resizable(False, True)


# Koin pemain dan pot
player_coins = 100  # Koin awal
bet_amount = 0
round_count = 1
pot = 0

# Membuat canvas sebagai meja
table_canvas = tk.Canvas(root, width=700, height=650, bg="dark green")
table_canvas.grid(row=0, column=0, columnspan=4, rowspan=10)


# Label untuk menampilkan saldo koin
player_coin_label = tk.Label(root, text=f"Your coins: {player_coins}", font=("Helvetica", 14), bg="dark green", fg="white")
player_coin_label.grid(row=0, column=0, padx=10, pady=10)

# Label untuk pot
pot_label = tk.Label(root, text=f"Pot: {pot} coins", font=("Helvetica", 14), bg="dark green", fg="white")
pot_label.grid(row=0, column=1, padx=10, pady=10)

# Label untuk hasil permainan
result_label = tk.Label(root, text="", font=("Helvetica", 16, 'bold'), bg="dark green", fg="white")
result_label.grid(row=0, column=2, columnspan=8, padx=10, pady=10)


# Input untuk memasukkan taruhan
bet_label = tk.Label(root, text="Place your bet:", font=("Helvetica", 14), bg="dark green", fg="white")
bet_label.grid(row=1, column=0, padx=10, pady=10)

bet_entry = tk.Entry(root, font=("Helvetica", 14))
bet_entry.grid(row=1, column=1, padx=10, pady=10)

bet_button = tk.Button(root, text="Place Bet", command=place_bet, font=("Helvetica", 14))
bet_button.grid(row=1, column=2, padx=10, pady=10)

# Tombol Start untuk memulai permainan
start_button = tk.Button(root, text="Start Game", command=start_game, font=("Helvetica", 14))
start_button.grid(row=1, column=3, padx=10, pady=10)

# Tombol untuk call
call_button = tk.Button(root, text="Call", command=call, font=("Helvetica", 14))
call_button.grid(row=2, column=3, padx=10, pady=10)

# Tombol untuk fold
fold_button = tk.Button(root, text="Fold", command=fold, font=("Helvetica", 14))
fold_button.grid(row=3, column=3, padx=10, pady=10)

raise_button = tk.Button(root, text="Raise", command=raise_bet, font=("Helvetica", 14))
raise_button.grid(row=4, column=3, padx=10, pady=10)

# Label untuk menampilkan taruhan yang sedang berlaku
bet_amount_label = tk.Label(root, text=f"Bet for round {round_count}: {bet_amount} coins", font=("Helvetica", 14), bg="dark green", fg="white")
bet_amount_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

# Label untuk menampilkan hasil
player_label = tk.Label(root, text="Your hand: ", font=("Helvetica", 14), bg="dark green", fg="white")
player_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# Canvas untuk gambar kartu pemain
player_canvas = tk.Canvas(root, width=350, height=150, bg="dark green")
player_canvas.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

# Canvas untuk gambar kartu dealer
dealer_label = tk.Label(root, text="Dealer's hand: ", font=("Helvetica", 14), bg="dark green", fg="white")
dealer_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

dealer_canvas = tk.Canvas(root, width=500, height=100, bg="dark green")
dealer_canvas.grid(row=6, column=0, columnspan=4, padx=10, pady=10)



# Tombol untuk memasukkan raise
raise_label = tk.Label(root, text="Enter raise amount:", font=("Helvetica", 14), bg="dark green", fg="white")
raise_label.grid(row=8, column=1, padx=10, pady=10)

raise_entry = tk.Entry(root, font=("Helvetica", 14))
raise_entry.grid(row=8, column=2, padx=10, pady=10)

footer_label = tk.Label(root, text="trappoker by: mirza kamal" , font=("college", 10), bg="black", fg="white")
footer_label.grid(row=10, column=0, padx=10, pady=10)



# Menjalankan aplikasi GUI
root.mainloop()