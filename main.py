import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import random
import string
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os
import json
import time

class BankingEncryptionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Hệ thống Mã hóa Ngân hàng")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Game state
        self.level = 1
        self.score = 0
        self.transactions_processed = 0
        self.current_transaction = None
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.timer_seconds = 30
        self.timer_running = False
        self.timer_id = None
        self.lich_su_giao_dich = []
        self.achievements = {
            "3_success": False,
            "1000_points": False,
            "level_5": False
        }
        self.success_streak = 0
        self.high_score = self.load_high_score()
        self.adaptive_timer = 30
        self.mini_game_counter = 0
        self.ten_nguoi_choi = self.nhap_ten_nguoi_choi()
        self.leaderboard = self.load_leaderboard()
        
        # Theme colors
        self.colors = {
            'primary': '#2c3e50',      # Dark blue
            'secondary': '#34495e',    # Lighter blue
            'success': '#27ae60',      # Green
            'warning': '#f39c12',      # Orange
            'danger': '#e74c3c',       # Red
            'info': '#3498db',         # Light blue
            'light': '#ecf0f1',        # Light gray
            'dark': '#2c3e50',         # Dark
            'white': '#ffffff',        # White
            'yellow': '#f1c40f'        # Yellow for timer
        }
        
        # Generate RSA keys
        self.generate_rsa_keys()
        
        # Create main interface
        self.create_interface()
        
        # Generate first transaction
        self.generate_new_transaction()
    
    def generate_rsa_keys(self):
        """Generate RSA key pair"""
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.rsa_public_key = self.rsa_private_key.public_key()
    
    def create_interface(self):
        """Create main game interface with improved design"""
        # Header với gradient effect
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Logo và title với style mới
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True)
        
        title_label = tk.Label(title_frame, text="🏦", font=('Arial', 24), 
                              fg=self.colors['white'], bg=self.colors['primary'])
        title_label.pack()
        
        title_text = tk.Label(title_frame, text="QUẢN TRỊ VIÊN BẢO MẬT NGÂN HÀNG", 
                             font=('Arial', 16, 'bold'), fg=self.colors['white'], 
                             bg=self.colors['primary'])
        title_text.pack()
        
        subtitle = tk.Label(title_frame, text="Bảo vệ giao dịch tài chính với công nghệ mã hóa tiên tiến", 
                           font=('Arial', 10), fg=self.colors['light'], 
                           bg=self.colors['primary'])
        subtitle.pack()
        
        # Status bar với design mới
        status_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=60)
        status_frame.pack(fill='x', padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        # Status items với style mới
        status_items = [
            (f"👤 {self.ten_nguoi_choi}", 'left'),
            (f"📊 Cấp độ: {self.level}", 'left'),
            (f"💰 Điểm: {self.score}", 'left'),
            (f"📈 Điểm cao nhất: {self.high_score}", 'right'),
            (f"⏰ Thời gian: {self.timer_seconds}s", 'right'),
            (f"🔄 Giao dịch: {self.transactions_processed}", 'right')
        ]
        
        for text, side in status_items:
            label = tk.Label(status_frame, text=text, font=('Arial', 11, 'bold'), 
                           fg=self.colors['white'], bg=self.colors['secondary'])
            label.pack(side=side, padx=15, pady=15)
            if 'Thời gian' in text:
                self.timer_label = label
            elif 'Cấp độ' in text:
                self.level_label = label
            elif 'Điểm:' in text and 'cao nhất' not in text:
                self.score_label = label
            elif 'Điểm cao nhất' in text:
                self.high_score_label = label
            elif 'Giao dịch:' in text:
                self.processed_label = label
        
        # Main content area với layout mới
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Transaction details với style mới
        left_frame = tk.LabelFrame(main_frame, text="🔄 Giao dịch mới cần xử lý", 
                                  font=('Arial', 12, 'bold'), bg=self.colors['light'], 
                                  fg=self.colors['primary'], relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Transaction display với style mới
        self.transaction_text = scrolledtext.ScrolledText(left_frame, height=12, width=45,
                                                         font=('Courier', 10), 
                                                         bg=self.colors['white'],
                                                         fg=self.colors['dark'],
                                                         relief='sunken', bd=1)
        self.transaction_text.pack(padx=15, pady=15, fill='both', expand=True)
        
        # Processing buttons với style mới và hover effects
        button_frame = tk.Frame(left_frame, bg=self.colors['light'])
        button_frame.pack(fill='x', padx=15, pady=10)
        
        # Button styles với hover effects
        button_styles = [
            ("🔐 Mã hóa AES", self.encrypt_aes, self.colors['info'], tk.NORMAL),
            ("✍️ Xác thực RSA", self.authenticate_rsa, self.colors['danger'], tk.DISABLED),
            ("🔍 Kiểm tra SHA", self.check_integrity_sha, self.colors['warning'], tk.DISABLED),
            ("✅ Hoàn tất giao dịch", self.complete_transaction, self.colors['success'], tk.DISABLED)
        ]
        
        self.buttons = {}
        for text, command, color, state in button_styles:
            btn = tk.Button(button_frame, text=text, command=command, 
                           bg=color, fg=self.colors['white'],
                           font=('Arial', 11, 'bold'), state=state,
                           relief='raised', bd=2, padx=20, pady=8)
            btn.pack(fill='x', pady=3)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, c, True))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_button_hover(b, c, False))
            
            # Store button references
            if 'AES' in text:
                self.aes_button = btn
            elif 'RSA' in text:
                self.rsa_button = btn
            elif 'SHA' in text:
                self.sha_button = btn
            elif 'Hoàn tất' in text:
                self.complete_button = btn
        
        # Right panel - Processing results với style mới
        right_frame = tk.LabelFrame(main_frame, text="📊 Kết quả xử lý và phản hồi", 
                                   font=('Arial', 12, 'bold'), bg=self.colors['light'], 
                                   fg=self.colors['primary'], relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Results display với style mới
        self.result_text = scrolledtext.ScrolledText(right_frame, height=18, width=55,
                                                    font=('Courier', 9), 
                                                    bg=self.colors['white'],
                                                    fg=self.colors['dark'],
                                                    relief='sunken', bd=1)
        self.result_text.pack(padx=15, pady=15, fill='both', expand=True)
        
        # Control buttons với style mới
        control_frame = tk.Frame(right_frame, bg=self.colors['light'])
        control_frame.pack(fill='x', padx=15, pady=10)
        
        # Control button styles
        control_buttons = [
            ("🔄 Giao dịch mới", self.generate_new_transaction, self.colors['info']),
            ("🗂 Lịch sử giao dịch", self.show_history, self.colors['warning']),
            ("🏆 Bảng xếp hạng", self.show_leaderboard, self.colors['success']),
            ("❓ Hướng dẫn", self.show_help, self.colors['secondary'])
        ]
        
        for text, command, color in control_buttons:
            btn = tk.Button(control_frame, text=text, command=command, 
                           bg=color, fg=self.colors['white'],
                           font=('Arial', 10, 'bold'), relief='raised', bd=2, padx=15, pady=5)
            btn.pack(side='left', padx=5)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, c, True))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_button_hover(b, c, False))
            
            # Store references
            if 'Giao dịch mới' in text:
                self.new_transaction_button = btn
            elif 'Lịch sử' in text:
                self.history_button = btn
            elif 'Bảng xếp hạng' in text:
                self.leaderboard_button = btn
            elif 'Hướng dẫn' in text:
                self.help_button = btn
    
    def generate_new_transaction(self):
        """Generate a new random transaction"""
        account_numbers = [f"{random.randint(1000000000, 9999999999)}" for _ in range(2)]
        amount = random.randint(100000, 50000000)
        
        self.current_transaction = {
            'id': f"TXN{random.randint(100000, 999999)}",
            'from_account': account_numbers[0],
            'to_account': account_numbers[1],
            'amount': amount,
            'description': f"Chuyển khoản {amount:,} VND",
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'encrypted_data': None,
            'rsa_signature': None,
            'sha_hash': None,
            'steps_completed': []
        }
        
        # Display transaction
        transaction_info = f"""
═══════════════════════════════════════
        GIAO DỊCH MỚI CẦN XỬ LÝ
═══════════════════════════════════════

ID Giao dịch: {self.current_transaction['id']}
Từ tài khoản: {self.current_transaction['from_account']}
Đến tài khoản: {self.current_transaction['to_account']}
Số tiền: {self.current_transaction['amount']:,} VND
Mô tả: {self.current_transaction['description']}
Thời gian: {self.current_transaction['timestamp']}

⚠️  TRẠNG THÁI: Chưa được bảo mật
⚠️  CẦN THỰC HIỆN: Mã hóa AES → Xác thực RSA → Kiểm tra SHA

═══════════════════════════════════════
"""
        
        self.transaction_text.delete(1.0, tk.END)
        self.transaction_text.insert(1.0, transaction_info)
        
        # Reset buttons
        self.aes_button.config(state='normal', bg='#3498db')
        self.rsa_button.config(state='disabled', bg='#bdc3c7')
        self.sha_button.config(state='disabled', bg='#bdc3c7')
        self.complete_button.config(state='disabled', bg='#bdc3c7')
        
        # Clear results
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, "🎯 Bắt đầu bằng việc mã hóa giao dịch với AES...\n\n")
        
        self.start_timer(self.adaptive_timer)
        self.mini_game_counter += 1
        if self.mini_game_counter % 3 == 0:
            self.show_mini_game()
    
    def encrypt_aes(self):
        """Encrypt transaction data using AES"""
        if not self.current_transaction:
            return
        
        # Create AES key
        aes_key = os.urandom(32)  # 256-bit key
        iv = os.urandom(16)  # 128-bit IV
        
        # Prepare data to encrypt
        data_to_encrypt = json.dumps({
            'id': self.current_transaction['id'],
            'from_account': self.current_transaction['from_account'],
            'to_account': self.current_transaction['to_account'],
            'amount': self.current_transaction['amount'],
            'timestamp': self.current_transaction['timestamp']
        }).encode('utf-8')
        
        # Encrypt using AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad data to be multiple of 16 bytes
        pad_length = 16 - (len(data_to_encrypt) % 16)
        padded_data = data_to_encrypt + bytes([pad_length] * pad_length)
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Store encrypted data
        self.current_transaction['encrypted_data'] = base64.b64encode(encrypted_data).decode('utf-8')
        self.current_transaction['aes_key'] = base64.b64encode(aes_key).decode('utf-8')
        self.current_transaction['aes_iv'] = base64.b64encode(iv).decode('utf-8')
        self.current_transaction['steps_completed'].append('AES')
        
        # Update UI
        result = f"""
🔐 MÃ HÓA AES THÀNH CÔNG!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Dữ liệu giao dịch đã được mã hóa bảo mật
🔑 Khóa AES: {self.current_transaction['aes_key'][:32]}...
🔢 IV: {self.current_transaction['aes_iv'][:32]}...
📦 Dữ liệu mã hóa: {self.current_transaction['encrypted_data'][:50]}...

⏩ BƯỚC TIẾP THEO: Xác thực RSA để đảm bảo tính xác thực

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        self.result_text.insert(tk.END, result)
        self.result_text.see(tk.END)
        
        # Enable next step
        self.aes_button.config(state='disabled', bg='#27ae60', text='✅ AES Hoàn tất')
        self.rsa_button.config(state='normal', bg='#e74c3c')
    
    def authenticate_rsa(self):
        """Authenticate transaction using RSA signature"""
        if not self.current_transaction or 'AES' not in self.current_transaction['steps_completed']:
            return
        
        # Create message to sign (transaction summary)
        message = f"{self.current_transaction['id']}{self.current_transaction['amount']}{self.current_transaction['timestamp']}"
        message_bytes = message.encode('utf-8')
        
        # Create RSA signature
        signature = self.rsa_private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        self.current_transaction['rsa_signature'] = base64.b64encode(signature).decode('utf-8')
        self.current_transaction['signed_message'] = message
        self.current_transaction['steps_completed'].append('RSA')
        
        # Verify signature (simulation)
        try:
            self.rsa_public_key.verify(
                signature,
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            verification_status = "✅ XÁC THỰC THÀNH CÔNG"
        except:
            verification_status = "❌ XÁC THỰC THẤT BẠI"
        
        # Update UI
        result = f"""
✍️ XÁC THỰC RSA THÀNH CÔNG!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Chữ ký số đã được tạo và xác thực
📝 Thông điệp ký: {message}
🔏 Chữ ký RSA: {self.current_transaction['rsa_signature'][:50]}...
{verification_status}

⏩ BƯỚC TIẾP THEO: Kiểm tra tính toàn vẹn bằng SHA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        self.result_text.insert(tk.END, result)
        self.result_text.see(tk.END)
        
        # Enable next step
        self.rsa_button.config(state='disabled', bg='#27ae60', text='✅ RSA Hoàn tất')
        self.sha_button.config(state='normal', bg='#f39c12')
    
    def check_integrity_sha(self):
        """Check transaction integrity using SHA hash"""
        if not self.current_transaction or 'RSA' not in self.current_transaction['steps_completed']:
            return
        
        # Create hash of the entire transaction data
        transaction_data = json.dumps({
            'id': self.current_transaction['id'],
            'encrypted_data': self.current_transaction['encrypted_data'],
            'rsa_signature': self.current_transaction['rsa_signature'],
            'timestamp': self.current_transaction['timestamp']
        }, sort_keys=True).encode('utf-8')
        
        # Generate SHA-256 hash
        sha_hash = hashlib.sha256(transaction_data).hexdigest()
        self.current_transaction['sha_hash'] = sha_hash
        self.current_transaction['steps_completed'].append('SHA')
        
        # Simulate integrity check
        verification_hash = hashlib.sha256(transaction_data).hexdigest()
        integrity_status = "✅ TÍNH TOÀN VẸN ĐẢM BẢO" if sha_hash == verification_hash else "❌ TÍNH TOÀN VẸN KHÔNG ĐẢM BẢO"
        
        # Update UI
        result = f"""
🔍 KIỂM TRA TÍNH TOÀN VẸN SHA THÀNH CÔNG!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Mã hash SHA-256 đã được tạo
🔗 Hash SHA-256: {sha_hash}
🔍 Kiểm tra: {integrity_status}

⏩ BƯỚC CUỐI: Hoàn tất giao dịch

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        self.result_text.insert(tk.END, result)
        self.result_text.see(tk.END)
        
        # Enable completion
        self.sha_button.config(state='disabled', bg='#27ae60', text='✅ SHA Hoàn tất')
        self.complete_button.config(state='normal', bg='#27ae60')
    
    def complete_transaction(self):
        """Complete the transaction and update score"""
        if not self.current_transaction or len(self.current_transaction['steps_completed']) != 3:
            return
        
        self.stop_timer()
        # Calculate score based on level and completion
        base_score = 100
        level_bonus = self.level * 50
        completion_bonus = 200 if len(self.current_transaction['steps_completed']) == 3 else 0
        
        earned_score = base_score + level_bonus + completion_bonus
        self.score += earned_score
        self.transactions_processed += 1
        
        # Adaptive difficulty: nếu người chơi làm tốt, giảm thời gian
        if self.success_streak >= 3 and self.adaptive_timer > 10:
            self.adaptive_timer -= 2
        
        # Lưu lịch sử giao dịch
        self.current_transaction['result'] = 'Thành công'
        self.current_transaction['score'] = earned_score
        self.lich_su_giao_dich.append(self.current_transaction.copy())
        
        # Cập nhật high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        # Thành tựu
        self.success_streak += 1
        self.check_achievements()
        
        # Thăng cấp
        if self.transactions_processed % 3 == 0:
            self.level += 1
            messagebox.showinfo("Thăng cấp!", f"🎉 Chúc mừng! Bạn đã lên cấp độ {self.level}!")
        
        self.update_status_bar()
        self.cap_nhat_leaderboard()
        
        result = f"""
🎉 GIAO DỊCH HOÀN TẤT!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Giao dịch {self.current_transaction['id']} đã được xử lý thành công!
🔐 Mã hóa AES: Hoàn tất
✍️ Xác thực RSA: Hoàn tất  
🔍 Kiểm tra SHA: Hoàn tất

💰 Điểm thưởng: +{earned_score} điểm
📊 Tổng điểm: {self.score} điểm
📈 Cấp độ: {self.level}

🔄 Nhấn 'Giao dịch mới' để tiếp tục...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        self.result_text.insert(tk.END, result)
        self.result_text.see(tk.END)
        
        # Disable all processing buttons
        self.complete_button.config(state='disabled', bg='#bdc3c7')
    
    def update_status_bar(self):
        """Update the status bar with current game state"""
        self.level_label.config(text=f"📊 Cấp độ: {self.level}")
        self.score_label.config(text=f"💰 Điểm: {self.score}")
        self.processed_label.config(text=f"🔄 Giao dịch: {self.transactions_processed}")
        self.high_score_label.config(text=f"📈 Điểm cao nhất: {self.high_score}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🏦 HƯỚNG DẪN GAME HỆ THỐNG MÃ HÓA NGÂN HÀNG

🎯 MỤC TIÊU:
Bạn là quản trị viên bảo mật ngân hàng. Nhiệm vụ của bạn là bảo vệ mọi giao dịch 
bằng cách thực hiện 3 bước bảo mật quan trọng.

🔄 CÁC BƯỚC XỬ LÝ:
1. 🔐 MÃ HÓA AES: Bảo vệ thông tin tài chính bằng mã hóa mạnh
2. ✍️ XÁC THỰC RSA: Tạo chữ ký số để xác thực giao dịch
3. 🔍 KIỂM TRA SHA: Đảm bảo tính toàn vẹn của dữ liệu

📊 HỆ THỐNG ĐIỂM:
- Mỗi bước hoàn thành: 100 điểm cơ bản
- Thưởng cấp độ: Cấp độ × 50 điểm
- Hoàn thành đủ 3 bước: +200 điểm thưởng
- Mỗi 3 giao dịch hoàn thành sẽ thăng cấp

⚡ TIPS:
- Phải hoàn thành các bước theo đúng thứ tự
- Càng lên cấp cao, giao dịch càng phức tạp
- Chú ý đọc kỹ thông tin từng bước để hiểu thuật toán

Chúc bạn bảo vệ thành công hệ thống ngân hàng! 🛡️
"""
        messagebox.showinfo("Hướng dẫn", help_text)

    def start_timer(self, seconds=None):
        if seconds is None:
            seconds = self.adaptive_timer
        self.timer_seconds = seconds
        self.timer_running = True
        self.update_timer_label()
        self.countdown()

    def countdown(self):
        if self.timer_running:
            self.timer_label.config(text=f"⏰ Thời gian: {self.timer_seconds}s")
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.timer_id = self.root.after(1000, self.countdown)
            else:
                self.timer_running = False
                self.timer_label.config(text="⏰ Hết giờ!")
                self.handle_timeout()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer_label(self):
        if hasattr(self, 'timer_label') and self.timer_label:
            self.timer_label.config(text=f"⏰ Thời gian: {self.timer_seconds}s")
            # Thay đổi màu khi thời gian sắp hết
            if self.timer_seconds <= 10:
                self.timer_label.config(fg='red')
            elif self.timer_seconds <= 20:
                self.timer_label.config(fg='orange')
            else:
                self.timer_label.config(fg=self.colors['yellow'])

    def load_high_score(self):
        try:
            if os.path.exists("highscore.json"):
                with open("highscore.json", "r") as f:
                    return json.load(f).get("high_score", 0)
        except:
            pass
        return 0

    def save_high_score(self):
        try:
            with open("highscore.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass

    def show_leaderboard(self):
        if not self.leaderboard:
            messagebox.showinfo("Bảng xếp hạng", "Chưa có người chơi nào.")
            return
        sorted_lb = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        text = "🏆 TOP 5 NGƯỜI CHƠI ĐIỂM CAO NHẤT:\n\n"
        for i, (ten, diem) in enumerate(sorted_lb[:5]):
            text += f"{i+1}. {ten}: {diem} điểm\n"
        messagebox.showinfo("Bảng xếp hạng", text)

    def show_history(self):
        if not self.lich_su_giao_dich:
            messagebox.showinfo("Lịch sử giao dịch", "Chưa có giao dịch nào được lưu.")
            return
        history_win = tk.Toplevel(self.root)
        history_win.title("Lịch sử giao dịch")
        history_win.geometry("600x400")
        lb = tk.Listbox(history_win, font=("Courier", 10))
        lb.pack(fill='both', expand=True)
        for idx, gd in enumerate(self.lich_su_giao_dich):
            lb.insert(tk.END, f"{idx+1}. {gd['id']} | {gd['amount']:,} VND | {gd['result']}")
        def show_detail(event):
            sel = lb.curselection()
            if sel:
                gd = self.lich_su_giao_dich[sel[0]]
                detail = json.dumps(gd, indent=2, ensure_ascii=False)
                messagebox.showinfo("Chi tiết giao dịch", detail)
        lb.bind('<Double-1>', show_detail)

    def handle_timeout(self):
        self.result_text.insert(tk.END, "\n⏰ HẾT GIỜ! Giao dịch bị hủy, bạn không được cộng điểm.\n")
        self.result_text.see(tk.END)
        self.aes_button.config(state='disabled')
        self.rsa_button.config(state='disabled')
        self.sha_button.config(state='disabled')
        self.complete_button.config(state='disabled')
        if self.current_transaction:
            self.current_transaction['result'] = 'Hết giờ'
            self.current_transaction['score'] = 0
            self.lich_su_giao_dich.append(self.current_transaction.copy())
        self.success_streak = 0
        if self.adaptive_timer < 30:
            self.adaptive_timer += 2

    def check_achievements(self):
        if not self.achievements["3_success"] and self.success_streak >= 3:
            self.achievements["3_success"] = True
            messagebox.showinfo("Thành tựu!", "🏅 Thành tựu: 3 giao dịch liên tiếp thành công!")
        if not self.achievements["1000_points"] and self.score >= 1000:
            self.achievements["1000_points"] = True
            messagebox.showinfo("Thành tựu!", "🏅 Thành tựu: Đạt 1000 điểm!")
        if not self.achievements["level_5"] and self.level >= 5:
            self.achievements["level_5"] = True
            messagebox.showinfo("Thành tựu!", "🏅 Thành tựu: Lên cấp 5!")

    def show_mini_game(self):
        mini_win = tk.Toplevel(self.root)
        mini_win.title("Mini-game bảo mật")
        mini_win.geometry("500x300")
        ds_cau_hoi = [
            ("Thuật toán nào dùng để kiểm tra tính toàn vẹn?", "SHA"),
            ("Thuật toán nào dùng để mã hóa đối xứng?", "AES"),
            ("Thuật toán nào dùng để xác thực chữ ký số?", "RSA"),
            ("Mã hóa nào nhanh hơn cho dữ liệu lớn?", "AES"),
            ("Chữ ký số dùng thuật toán nào?", "RSA"),
            ("Thuật toán nào KHÔNG phải là mã hóa đối xứng?", "RSA"),
            ("SHA là viết tắt của?", "Secure Hash Algorithm"),
            ("AES là viết tắt của?", "Advanced Encryption Standard"),
            ("RSA là viết tắt của tên 3 nhà khoa học nào?", "Rivest Shamir Adleman"),
            ("Thuật toán nào dùng khóa công khai và khóa bí mật?", "RSA"),
            ("Thuật toán nào thường dùng để mã hóa mật khẩu lưu trữ?", "SHA"),
            ("ECC là viết tắt của?", "Elliptic Curve Cryptography"),
            ("Blockchain dùng thuật toán băm nào phổ biến?", "SHA256"),
            ("Thuật toán nào KHÔNG dùng trong game này?", "DES"),
            ("Thuật toán nào có thể dùng để tạo chữ ký số?", "RSA"),
            ("Thuật toán nào có thể kiểm tra dữ liệu bị thay đổi?", "SHA"),
            ("AES thuộc loại mã hóa nào?", "Đối xứng"),
            ("RSA thuộc loại mã hóa nào?", "Bất đối xứng"),
            ("SHA có thể giải mã được không?", "Không"),
            ("Mã hóa đồng cấu là gì?", "Homomorphic encryption"),
        ]
        q, a = random.choice(ds_cau_hoi)
        tk.Label(mini_win, text=q, font=("Arial", 12, "bold"), wraplength=480).pack(pady=10)
        ans_var = tk.StringVar()
        entry = tk.Entry(mini_win, textvariable=ans_var, font=("Arial", 12))
        entry.pack(pady=10)
        def check_answer():
            if ans_var.get().strip().lower() == a.lower():
                messagebox.showinfo("Mini-game", "🎉 Đúng! Bạn được cộng 100 điểm!")
                self.score += 100
                self.update_status_bar()
                self.cap_nhat_leaderboard()
                mini_win.destroy()
            else:
                messagebox.showwarning("Mini-game", "❌ Sai! Đáp án đúng là: " + a)
                mini_win.destroy()
        tk.Button(mini_win, text="Trả lời", command=check_answer, font=("Arial", 11, "bold"), bg="#27ae60", fg="white").pack(pady=10)
        entry.focus()

    def nhap_ten_nguoi_choi(self):
        ten = None
        while not ten:
            ten = tk.simpledialog.askstring("Tên người chơi", "Nhập tên của bạn:")
            if ten is None or ten.strip() == "":
                messagebox.showwarning("Cảnh báo", "Bạn phải nhập tên để chơi!")
                ten = None
        return ten.strip()

    def load_leaderboard(self):
        try:
            if os.path.exists("leaderboard.json"):
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def save_leaderboard(self):
        try:
            with open("leaderboard.json", "w", encoding="utf-8") as f:
                json.dump(self.leaderboard, f, ensure_ascii=False, indent=2)
        except:
            pass

    def cap_nhat_leaderboard(self):
        ten = self.ten_nguoi_choi
        diem = self.score
        if ten in self.leaderboard:
            if diem > self.leaderboard[ten]:
                self.leaderboard[ten] = diem
        else:
            self.leaderboard[ten] = diem
        self.save_leaderboard()

    def on_button_hover(self, button, original_color, entering):
        if entering:
            # Lighter color on hover
            lighter_color = self.lighten_color(original_color, 20)
            button.config(bg=lighter_color)
        else:
            button.config(bg=original_color)
    
    def lighten_color(self, color, percent):
        """Lighten a color by a percentage"""
        # Simple color lightening - you can implement more sophisticated color manipulation
        if color == self.colors['info']:
            return '#5dade2'
        elif color == self.colors['danger']:
            return '#ec7063'
        elif color == self.colors['warning']:
            return '#f7dc6f'
        elif color == self.colors['success']:
            return '#58d68d'
        else:
            return color

def main():
    """Main function to run the game"""
    root = tk.Tk()
    game = BankingEncryptionGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()