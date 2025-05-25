import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import io
import tempfile
import webbrowser
import platform

class DigitalArrestScamTraining:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Arrest Scam Training")
        self.root.geometry("800x600")
        self.root.minsize(700, 550)
        
        # Configure the theme colors
        self.bg_color = "#f5f5f5"
        self.header_bg = "#0046b8"
        self.header_fg = "white"
        self.primary_btn_color = "#0046b8"
        self.secondary_btn_color = "#f5f5f5"
        self.btn_text_color = "white"
        self.option_bg = "#f9f9f9"
        self.option_border = "#e0e0e0"
        self.selected_bg = "#e3f2fd"
        self.selected_border = "#2979ff"
        self.correct_bg = "#e8f5e9"
        self.correct_border = "#00c853"
        self.incorrect_bg = "#ffebee"
        self.incorrect_border = "#ff3d00"
        
        # Quiz data
        self.current_step = 0
        self.total_steps = 15  # 0 (user info) + 13 (questions) + 1 (certificate)
        self.selected_options = {}
        self.answered_correctly = {}
        self.feedback_visible = False
        
        self.correct_answers = {
            1: 2,  # Scenario 1: correct answer is option 2
            2: 3,  # Scenario 2: correct answer is option 3
            3: 0,  # Scenario 3: correct answer is option 0
            4: 2,  # Scenario 4: correct answer is option 2
            5: 1,  # Scenario 5: correct answer is option 1
            6: 2,  # Scenario 6: correct answer is option 2
            7: 2,  # Scenario 7: correct answer is option 2
            8: 1,  # Scenario 8: correct answer is option 1
            9: 2,  # Scenario 9: correct answer is option 2
            10: 0, # Scenario 10: correct answer is option 0
            11: 2, # Scenario 11: correct answer is option 2
            12: 0, # Scenario 12: correct answer is option 0
            13: 1, # Scenario 13: correct answer is option 1
        }
        
        self.questions = {
            1: "You receive a call from someone claiming to be from CBI. They say your Aadhaar number was used in illegal activities and you must pay a fee to avoid arrest. What should you do?",
            2: "A person in uniform appears on a video call claiming to be from Income Tax Department. They show an 'arrest warrant' with your name. What is a sign this is a scam?",
            3: "Which action should you take if you suspect a digital arrest scam?",
            4: "You receive an SMS stating your bank account will be frozen due to \"illegal transactions\" unless you click on a link. What should you do?",
            5: "A caller claiming to be from the Enforcement Directorate asks you to download a remote access app so they can \"verify your device is clean.\" This is:",
            6: "Which of these is NOT a warning sign of a digital arrest scam?",
            7: "You receive a WhatsApp video call from someone claiming to be a police officer. During the call, they show you a warrant and demand payment. What is the best response?",
            8: "Which of these agencies is commonly impersonated in digital arrest scams in India?",
            9: "A caller says they're from the Income Tax Department and claims you're under investigation. They offer to close the case if you pay a \"settlement fee.\" What's the correct action?",
            10: "Your elderly parent receives a digital arrest scam call. What is the most important step to take with them?",
            11: "What information should you NEVER share with someone who calls claiming to be from a government agency?",
            12: "A legitimate government communication about legal matters will typically:",
            13: "Which of the following is a secure way to verify if a call from a government agency is legitimate?"
        }
        
        self.options = {
            1: ["Pay the fee immediately to avoid trouble", 
                "Provide your bank details so they can verify your identity", 
                "Hang up and report the call to the official CBI website or local police", 
                "Call back on the number they provide to confirm"],
            2: ["Government officials never conduct video calls for legal matters", 
                "They demand immediate payment via digital wallets or cryptocurrency", 
                "They refuse to provide a callback number to official department", 
                "All of the above"],
            3: ["Call 1930 (National Cyber Crime Helpline) to report", 
                "Share the caller's details with friends to warn them", 
                "Visit the nearest police station immediately", 
                "Ask the caller for more information to verify"],
            4: ["Click the link to verify your account details", 
                "Reply to the SMS asking for more details", 
                "Ignore the SMS and contact your bank directly through their official phone number", 
                "Forward the SMS to your friends to check if they received it too"],
            5: ["A legitimate procedure to avoid legal issues", 
                "A scam to gain access to your device and personal information", 
                "A routine security check that all citizens must comply with", 
                "Safe if they show government ID first"],
            6: ["The caller creates a sense of urgency and fear", 
                "They threaten immediate arrest if you don't comply", 
                "They provide official ID numbers and ask you to verify them on the government website", 
                "They request payment through cryptocurrency or gift cards"],
            7: ["Record the call as evidence and then disconnect", 
                "Ask them to email you the warrant for verification", 
                "Disconnect immediately and report to the cyber crime portal", 
                "Negotiate a lower payment amount"],
            8: ["Ministry of Tourism", 
                "Central Bureau of Investigation (CBI)", 
                "Department of Agriculture", 
                "Sports Authority of India"],
            9: ["Pay a small amount to see if they close the case", 
                "Ask them to email official documentation and then decide", 
                "Hang up and report to the Income Tax Department through official channels", 
                "Provide your PAN card details so they can verify it's really you"],
            10: ["Talk to them about common scam techniques and warning signs", 
                 "Take away their phone to prevent future scam calls", 
                 "Tell them to never answer calls from unknown numbers", 
                 "Report the incident but don't discuss it to avoid frightening them"],
            11: ["Your name", 
                 "Your city of residence", 
                 "OTP received on your phone", 
                 "The current date"],
            12: ["Come through official postal mail or registered courier service", 
                 "Ask for immediate payment through digital wallets", 
                 "Threaten arrest within 24 hours if you don't comply", 
                 "Come through WhatsApp from international numbers"],
            13: ["Ask the caller for their personal mobile number to call back", 
                 "Hang up and call the official published number of the agency from their website", 
                 "Request the caller to send an email from a gmail.com address", 
                 "Check if the caller has a government official's photo on their WhatsApp profile"]
        }
        
        self.feedback_messages = {
            "correct": [
                "Excellent choice! You've identified the correct approach to stay safe.",
                "That's right! This is the best way to protect yourself from digital arrest scams.",
                "Perfect! This knowledge will help you stay safe from scammers.",
                "Correct! You're showing good awareness of digital safety practices."
            ],
            "incorrect": [
                "Be careful! This choice could make you vulnerable to scammers.",
                "That's not the safest approach. Remember, government agencies don't operate this way.",
                "Incorrect. This action could put your personal information or money at risk.",
                "That's not right. This response might lead to identity theft or financial loss."
            ]
        }
        
        # Setup UI
        self.setup_ui()
        self.show_step(self.current_step)
        self.update_progress()
    
    def setup_ui(self):
        self.root.configure(bg=self.bg_color)
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        self.header_frame = tk.Frame(self.main_frame, bg=self.header_bg, padx=20, pady=20)
        self.header_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(self.header_frame, 
                                    text="Digital Arrest Scam Training", 
                                    font=("Segoe UI", 18, "bold"), 
                                    bg=self.header_bg, 
                                    fg=self.header_fg)
        self.title_label.pack(anchor=tk.W)
        
        self.subtitle_label = tk.Label(self.header_frame, 
                                       text="Test your knowledge about digital arrest scams and learn how to protect yourself. Complete all scenarios to earn your Digital Safety Certificate.", 
                                       font=("Segoe UI", 10), 
                                       bg=self.header_bg, 
                                       fg=self.header_fg, 
                                       wraplength=760, 
                                       justify=tk.LEFT)
        self.subtitle_label.pack(anchor=tk.W, pady=(5, 15))
        
        # Progress bar
        self.progress_frame = tk.Frame(self.header_frame, bg=self.header_bg)
        self.progress_frame.pack(fill=tk.X)
        
        self.progress_container = tk.Frame(self.progress_frame, bg="white", height=6, borderwidth=0)
        self.progress_container.pack(fill=tk.X)
        
        self.progress_bar = tk.Frame(self.progress_container, bg="#00c853", height=6, width=0, borderwidth=0)
        self.progress_bar.place(relx=0, rely=0, relheight=1.0, relwidth=0)
        
        # Body frame with scrolling
        self.body_canvas = tk.Canvas(self.main_frame, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.body_canvas.yview)
        self.body_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.body_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.card_body = ttk.Frame(self.body_canvas)
        self.body_canvas.create_window((0, 0), window=self.card_body, anchor=tk.NW, tags="self.card_body")
        
        # Create all step frames
        self.step_frames = {}
        
        # Step 0: User Info
        self.step_frames[0] = ttk.Frame(self.card_body, padding=30)
        tk.Label(self.step_frames[0], text="Start Your Digital Safety Training", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        tk.Label(self.step_frames[0], text="Please enter your name to begin the training. Your name will appear on your completion certificate.", wraplength=700).pack(anchor=tk.W, pady=(0, 20))
        
        name_frame = ttk.Frame(self.step_frames[0])
        name_frame.pack(fill=tk.X, pady=5)
        tk.Label(name_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(name_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        email_frame = ttk.Frame(self.step_frames[0])
        email_frame.pack(fill=tk.X, pady=5)
        tk.Label(email_frame, text="Email (Optional):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(email_frame, width=40)
        self.email_entry.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # Question Steps (1-13)
        for q_num in range(1, 14):
            self.step_frames[q_num] = ttk.Frame(self.card_body, padding=30)
            
            # Question text
            question_text = self.questions[q_num]
            question_label = tk.Label(self.step_frames[q_num], 
                                     text=question_text, 
                                     font=("Segoe UI", 11, "bold"), 
                                     wraplength=700, 
                                     justify=tk.LEFT)
            question_label.pack(anchor=tk.W, pady=(0, 20))
            
            # Options frame
            options_frame = ttk.Frame(self.step_frames[q_num], padding=0)
            options_frame.pack(fill=tk.X)
            
            # Create option buttons
            self.option_buttons = []
            for i, option_text in enumerate(self.options[q_num]):
                option_frame = tk.Frame(options_frame, 
                                         bg=self.option_bg, 
                                         highlightbackground=self.option_border, 
                                         highlightthickness=2,
                                         padx=15, pady=15, 
                                         cursor="hand2")
                option_frame.pack(fill=tk.X, pady=6, ipady=3)
                option_frame.option_value = i
                option_frame.question_num = q_num
                
                option_label = tk.Label(option_frame, 
                                        text=option_text, 
                                        bg=self.option_bg, 
                                        wraplength=650, 
                                        justify=tk.LEFT)
                option_label.pack(anchor=tk.W)
                
                # Bind click events
                option_frame.bind("<Button-1>", self.select_option)
                option_label.bind("<Button-1>", lambda e, frame=option_frame: self.select_option(tk.Event(), frame))
                
                # Store references to frames
                if not hasattr(self, f'option_frames_{q_num}'):
                    setattr(self, f'option_frames_{q_num}', [])
                getattr(self, f'option_frames_{q_num}').append(option_frame)
            
            # Feedback area
            feedback_frame = tk.Frame(self.step_frames[q_num], bg=self.bg_color, padx=15, pady=15)
            feedback_frame.pack(fill=tk.X, pady=(20, 0))
            
            feedback_label = tk.Label(feedback_frame, 
                                     text="", 
                                     wraplength=650, 
                                     justify=tk.LEFT)
            feedback_label.pack(anchor=tk.W)
            
            # Store reference to feedback
            setattr(self, f'feedback_frame_{q_num}', feedback_frame)
            setattr(self, f'feedback_label_{q_num}', feedback_label)
            
            # Initially hide feedback
            feedback_frame.pack_forget()
        
        # Step 14: Certificate
        self.step_frames[14] = ttk.Frame(self.card_body, padding=30)
        self.setup_certificate_ui()
        
        # Footer frame
        self.footer_frame = tk.Frame(self.main_frame, bg="white", padx=20, pady=20)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Footer buttons
        self.prev_btn = ttk.Button(self.footer_frame, text="Previous", command=self.previous_step, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT)
        
        self.next_btn = ttk.Button(self.footer_frame, text="Start Training", command=self.next_step)
        self.next_btn.pack(side=tk.RIGHT)
        
        # Bind resize event
        self.card_body.bind("<Configure>", self.on_frame_configure)
        self.body_canvas.bind("<Configure>", self.on_canvas_configure)
        
    def on_frame_configure(self, event):
        self.body_canvas.configure(scrollregion=self.body_canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.body_canvas.itemconfig("self.card_body", width=canvas_width)
    
    def update_progress(self):
        progress = (self.current_step / (self.total_steps - 1))
        self.progress_bar.place(relwidth=progress)
    
    def select_option(self, event=None, option_frame=None):
        if option_frame is None:
            option_frame = event.widget
        
        q_num = option_frame.question_num
        value = option_frame.option_value
        
        # Reset all options in this step
        for frame in getattr(self, f'option_frames_{q_num}'):
            frame.config(bg=self.option_bg, highlightbackground=self.option_border)
            for child in frame.winfo_children():
                child.config(bg=self.option_bg)
        
        # Mark selected option
        option_frame.config(bg=self.selected_bg, highlightbackground=self.selected_border)
        for child in option_frame.winfo_children():
            child.config(bg=self.selected_bg)
        
        # Store selection
        self.selected_options[q_num] = value
        
        # Enable next button
        self.next_btn.config(state=tk.NORMAL)
        
        # Hide any existing feedback
        feedback_frame = getattr(self, f'feedback_frame_{q_num}')
        feedback_frame.pack_forget()
        self.feedback_visible = False
    
    def show_step(self, step):
        # Hide all steps
        for frame in self.step_frames.values():
            frame.pack_forget()
        
        # Show current step
        self.step_frames[step].pack(fill=tk.BOTH, expand=True)
        
        # Reset feedback status
        self.feedback_visible = False
        
        # Update buttons
        self.prev_btn.config(state=tk.NORMAL if step > 0 else tk.DISABLED)
        
        if step == 0:
            self.next_btn.config(text="Start Training", 
                                state=tk.NORMAL if self.name_entry.get().strip() else tk.DISABLED)
            # Bind to entry change
            self.name_entry.bind("<KeyRelease>", self.check_name_entry)
        elif step == 14:
            # Certificate step
            self.next_btn.config(text="Finish", state=tk.NORMAL, command=self.finish_training)
            self.generate_certificate()
        else:
            self.next_btn.config(text="Next")
            
            # Check if an option has been selected
            if step >= 1 and step <= 13:
                self.next_btn.config(state=tk.NORMAL if step in self.selected_options else tk.DISABLED)
            else:
                self.next_btn.config(state=tk.NORMAL)
        
        # Reset scroll position
        self.body_canvas.yview_moveto(0)
    
    def check_name_entry(self, event=None):
        self.next_btn.config(state=tk.NORMAL if self.name_entry.get().strip() else tk.DISABLED)
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)
            self.update_progress()
    
    def next_step(self):
        # Handle user info step
        if self.current_step == 0:
            name_value = self.name_entry.get().strip()
            if not name_value:
                messagebox.showinfo("Input Required", "Please enter your name to continue.")
                return
            
            # Proceed to next step
            self.current_step += 1
            self.show_step(self.current_step)
            self.update_progress()
            return
        
        # Handle question steps
        if 1 <= self.current_step <= 13:
            # If feedback is not visible, check answer first
            if not self.feedback_visible:
                is_correct = self.check_answer()
                
                # Show feedback
                feedback_frame = getattr(self, f'feedback_frame_{self.current_step}')
                feedback_frame.pack(fill=tk.X, pady=(20, 0))
                self.feedback_visible = True
                
                # Stop here if incorrect, let user see the feedback
                if not is_correct:
                    return
            
            # If we're here, feedback is visible and answer was correct OR
            # feedback is visible and user clicked next again
            self.feedback_visible = False
        
        # Move to next step if not at last step
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.show_step(self.current_step)
            self.update_progress()
    
    def check_answer(self):
        if not (1 <= self.current_step <= 13):
            return False
        
        selected = self.selected_options.get(self.current_step)
        if selected is None:
            return False
        
        correct = self.correct_answers[self.current_step]
        feedback_frame = getattr(self, f'feedback_frame_{self.current_step}')
        feedback_label = getattr(self, f'feedback_label_{self.current_step}')
        
        option_frames = getattr(self, f'option_frames_{self.current_step}')
        selected_frame = option_frames[selected]
        correct_frame = option_frames[correct]
        
        # Mark as answered correctly if correct
        if selected == correct:
            self.answered_correctly[self.current_step] = True
            feedback_frame.config(bg=self.correct_bg)
            feedback_label.config(
                text=random.choice(self.feedback_messages["correct"]),
                bg=self.correct_bg, 
                fg="#2e7d32"
            )
            selected_frame.config(bg=self.correct_bg, highlightbackground=self.correct_border)
            for child in selected_frame.winfo_children():
                child.config(bg=self.correct_bg)
            return True
        else:
            self.answered_correctly[self.current_step] = False
            feedback_frame.config(bg=self.incorrect_bg)
            feedback_label.config(
                text=random.choice(self.feedback_messages["incorrect"]),
                bg=self.incorrect_bg, 
                fg="#c62828"
            )
            selected_frame.config(bg=self.incorrect_bg, highlightbackground=self.incorrect_border)
            for child in selected_frame.winfo_children():
                child.config(bg=self.incorrect_bg)
            
            # Highlight correct answer
            correct_frame.config(bg=self.correct_bg, highlightbackground=self.correct_border)
            for child in correct_frame.winfo_children():
                child.config(bg=self.correct_bg)
            return False
    
    def setup_certificate_ui(self):
        certificate_frame = ttk.Frame(self.step_frames[14], padding=0)
        certificate_frame.pack(fill=tk.BOTH, expand=True)
        
        # Certificate
        self.certificate_container = tk.Frame(certificate_frame, bg="white", padx=20, pady=20, 
                                           highlightbackground=self.primary_btn_color, highlightthickness=10)
        self.certificate_container.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(self.certificate_container, text="DIGITAL SAFETY CERTIFICATE", 
                font=("Segoe UI", 16, "bold"), bg="white", fg=self.primary_btn_color).pack(pady=(10, 5))
        
        tk.Label(self.certificate_container, text="This certifies that", 
                font=("Segoe UI", 10), bg="white").pack(pady=5)
        
        self.certificate_name = tk.Label(self.certificate_container, text="Your Name", 
                                      font=("Segoe UI", 18, "bold"), bg="white", fg="#003894")
        self.certificate_name.pack(pady=5)
        
        tk.Label(self.certificate_container, text="has successfully completed the", 
                font=("Segoe UI", 10), bg="white").pack(pady=2)
        
        tk.Label(self.certificate_container, text="Digital Arrest Scam Prevention Training Program", 
                font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)
        
        tk.Label(self.certificate_container, text="demonstrating knowledge and skills to identify, avoid, and report digital arrest scams", 
                font=("Segoe UI", 10), bg="white", wraplength=500).pack(pady=5)
        
        self.score_display = tk.Label(self.certificate_container, text="Score: 0/13", 
                                   font=("Segoe UI", 12), bg="white", fg=self.primary_btn_color)
        self.score_display.pack(pady=10)
        
        self.certificate_date = tk.Label(self.certificate_container, text="May 6, 2025", 
                                      font=("Segoe UI", 10, "italic"), bg="white", fg="#666666")
        self.certificate_date.pack(pady=20)
        
        signature_frame = tk.Frame(self.certificate_container, bg="white", padx=20, pady=10, 
                                  highlightbackground="#ccc", highlightthickness=1, highlightcolor="#ccc")
        signature_frame.pack(pady=10)
        
        tk.Label(signature_frame, text="Training Program Director", 
                font=("Segoe UI", 10, "bold"), bg="white").pack()
        
        # Seal (simplified)
        seal_frame = tk.Frame(self.certificate_container, bg=self.primary_btn_color, width=80, height=80, 
                             borderwidth=0, relief="raised")
        seal_frame.place(relx=0.85, rely=0.8)
        seal_frame.pack_propagate(False)
        
        tk.Label(seal_frame, text="CERTIFIED", font=("Segoe UI", 10, "bold"), 
                bg=self.primary_btn_color, fg="white").pack(expand=True)
        
        # Key Learnings
        details_frame = tk.Frame(certificate_frame, bg="#f9f9f9", padx=15, pady=15, 
                               highlightbackground="#eee", highlightthickness=1)
        details_frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(details_frame, text="Key Learnings:", font=("Segoe UI", 11, "bold"), 
                bg="#f9f9f9").pack(anchor=tk.W)
        
        learnings = [
            "Recognize common tactics used in digital arrest scams",
            "Verify the authenticity of communication from government agencies",
            "Protect sensitive personal and financial information",
            "Report suspicious communication to appropriate authorities",
            "Educate others about digital safety measures"
        ]
        
        for learning in learnings:
            learning_frame = tk.Frame(details_frame, bg="#f9f9f9")
            learning_frame.pack(fill=tk.X, pady=2, anchor=tk.W)
            
            tk.Label(learning_frame, text="•", bg="#f9f9f9").pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(learning_frame, text=learning, bg="#f9f9f9", anchor=tk.W, 
                    justify=tk.LEFT, wraplength=600).pack(side=tk.LEFT, fill=tk.X)
        
        # Print button
        self.print_btn = ttk.Button(certificate_frame, text="Save Certificate", command=self.save_certificate)
        self.print_btn.pack(pady=20)
        
        # Share info
        tk.Label(certificate_frame, text="Share this training with friends and family to help them stay safe too!", 
                font=("Segoe UI", 9), fg="#666666").pack(pady=5)
        
        # Add a button to download the certificate
        self.download_btn = ttk.Button(certificate_frame, text="Download the Certificate", command=self.save_certificate)
        self.download_btn.pack(pady=10)
    
    def generate_certificate(self):
        # Calculate score
        correct_count = sum(1 for v in self.answered_correctly.values() if v is True)
        total_questions = 13
        
        # Get the user's name from input
        name = self.name_entry.get().strip() or "Participant"
        
        # Set certificate details
        self.certificate_name.config(text=name)
        self.score_display.config(text=f"Score: {correct_count}/{total_questions}")
        
        # Set current date
        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")
        self.certificate_date.config(text=formatted_date)
    
    def save_certificate(self):
        # Generate certificate image
        name = self.name_entry.get().strip() or "Participant"
        correct_count = sum(1 for v in self.answered_correctly.values() if v is True)
        total_questions = 13
        today = datetime.now()
        formatted_date = today.strftime("%B %d, %Y")

        # Create a blank image for the certificate
        cert_width, cert_height = 800, 600
        cert_image = Image.new("RGB", (cert_width, cert_height), "white")
        draw = ImageDraw.Draw(cert_image)

        # Load a font
        try:
            # Attempt to load the Arial font from the system fonts directory
            font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arial.ttf')
            title_font = ImageFont.truetype(font_path, 40)
            name_font = ImageFont.truetype(font_path, 30)
            text_font = ImageFont.truetype(font_path, 20)
        except IOError:
            # Use a default PIL font if Arial is not found
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            messagebox.showwarning("Font Warning", "The Arial font could not be loaded. Using default font instead.")

        # Debugging: Log the font path being used
        print(f"Font path used: {font_path}")

        # Draw certificate content
        draw.text((cert_width // 2, 50), "DIGITAL SAFETY CERTIFICATE", font=title_font, fill="black", anchor="mm")
        draw.text((cert_width // 2, 150), f"This certifies that", font=text_font, fill="black", anchor="mm")
        draw.text((cert_width // 2, 200), name, font=name_font, fill="blue", anchor="mm")
        draw.text((cert_width // 2, 250), "has successfully completed the", font=text_font, fill="black", anchor="mm")
        draw.text((cert_width // 2, 300), "Digital Arrest Scam Prevention Training Program", font=text_font, fill="black", anchor="mm")
        draw.text((cert_width // 2, 350), f"Score: {correct_count}/{total_questions}", font=text_font, fill="green", anchor="mm")
        draw.text((cert_width // 2, 400), formatted_date, font=text_font, fill="black", anchor="mm")

        # Save the certificate to a temporary file
        try:
            temp_dir = tempfile.gettempdir()
            cert_path = os.path.join(temp_dir, f"{name}_certificate.png")
            cert_image.save(cert_path)

            # Notify the user and open the file
            messagebox.showinfo("Certificate Downloaded", f"Your certificate has been saved to: {cert_path}")
            webbrowser.open(cert_path)
        except Exception as e:
            # Log the error and notify the user
            print(f"Error saving certificate: {e}")
            messagebox.showerror("Save Error", f"An error occurred while saving the certificate: {e}")

    def finish_training(self):
        # Display a thank-you message and close the application
        messagebox.showinfo("Training Complete", "Thank you for completing the Digital Arrest Scam Training!")
        self.root.destroy()

def main():
    root = tk.Tk()
    app = DigitalArrestScamTraining(root)
    root.mainloop()

if __name__ == "__main__":
    main()