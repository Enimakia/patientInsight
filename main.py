import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import email_config  # Ensure this import is correct

# Load email configuration
SMTP_SERVER = email_config.SMTP_SERVER
SMTP_PORT = email_config.SMTP_PORT
SENDER_EMAIL = email_config.SENDER_EMAIL
SENDER_PASSWORD = email_config.SENDER_PASSWORD
DOCTOR_EMAIL = email_config.DOCTOR_EMAIL

# Load symptom-to-cause mapping
symptom_causes = {
    "Headache": ["Stress", "Dehydration", "Migraine", "Sinus infection", "Tension", "Cluster headache"],
    "Fever": ["Viral infection", "Bacterial infection", "Inflammation", "Heatstroke", "Medication reaction"],
    "Cough": ["Common cold", "Flu", "Allergies", "Asthma", "Chronic bronchitis", "Pneumonia"],
    "Fatigue": ["Lack of sleep", "Anemia", "Depression", "Chronic fatigue syndrome", "Hypothyroidism", "Sleep apnea"],
    "Nausea": ["Food poisoning", "Pregnancy", "Motion sickness", "Migraine", "Gastritis", "Medication side effect"],
    "Joint pain": ["Arthritis", "Injury", "Gout", "Fibromyalgia", "Tendinitis", "Rheumatoid arthritis"],
    "Chest pain": ["Heart attack", "Angina", "Pneumonia", "Acid reflux", "Pulmonary embolism", "Muscle strain"],
    "Shortness of breath": ["Asthma", "Chronic obstructive pulmonary disease (COPD)", "Heart failure",
                            "Pulmonary embolism", "Pneumonia", "Anxiety"],
    "Dizziness": ["Vertigo", "Low blood pressure", "Dehydration", "Inner ear infection", "Medication side effect",
                  "Anxiety"],
    "Abdominal pain": ["Gastritis", "Appendicitis", "Irritable bowel syndrome (IBS)", "Ulcer", "Gallstones",
                       "Constipation"],
    "Skin rash": ["Allergic reaction", "Eczema", "Psoriasis", "Impetigo", "Contact dermatitis", "Shingles"],
    "Back pain": ["Muscle strain", "Herniated disc", "Spinal stenosis", "Osteoarthritis", "Scoliosis", "Kidney stones"],
    "Swelling": ["Edema", "Injury", "Heart failure", "Kidney disease", "Infection", "Lymphedema"],
    "Insomnia": ["Stress", "Anxiety", "Depression", "Sleep apnea", "Medication side effect", "Caffeine"],
    "Memory loss": ["Alzheimer's disease", "Dementia", "Stroke", "Vitamin deficiency", "Medication side effect",
                    "Traumatic brain injury"],
    "Weight loss": ["Hyperthyroidism", "Diabetes", "Cancer", "Chronic infection", "Malabsorption", "Depression"],
    "Frequent urination": ["Diabetes", "Urinary tract infection (UTI)", "Prostate problems", "Pregnancy",
                           "Overactive bladder", "Medications"],
    "Numbness": ["Peripheral neuropathy", "Stroke", "Multiple sclerosis", "Diabetes", "Vitamin deficiency",
                 "Nerve compression"],
    "Hearing loss": ["Ear infection", "Age-related hearing loss", "Noise-induced hearing loss", "Meniere's disease",
                     "Otosclerosis", "Medication side effect"]
}


def get_possible_causes():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    location = location_entry.get()
    symptoms = symptoms_text.get("1.0", tk.END).strip().split(",")

    # Convert symptoms to title case for case-insensitive matching
    symptoms = [symptom.strip().title() for symptom in symptoms]

    # Print debug information
    print(f"Input values:\nName: {name}\nAge: {age}\nGender: {gender}\nLocation: {location}\nSymptoms: {symptoms}")
    print(f"Dictionary keys: {list(symptom_causes.keys())}")

    if not name or not age or not gender or not location or not symptoms:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    result = f"Patient Information:\nName: {name}\nAge: {age}\nGender: {gender}\nLocation: {location}\n\nPossible causes based on symptoms:\n"

    for symptom in symptoms:
        # Make sure the symptom is title-cased before checking
        if symptom in symptom_causes:
            causes = symptom_causes[symptom]
            result += f"\n{symptom}:\n- " + "\n- ".join(causes)
        else:
            result += f"\n{symptom}: Unknown cause"

    print(f"Generated result:\n{result}")

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result)

    # Store in database
    conn = sqlite3.connect('patient_records.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO patients (name, age, gender, location, symptoms, analysis, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, age, gender, location, ", ".join(symptoms), result, timestamp))
    conn.commit()
    conn.close()

    print("Patient data stored in database.")

    # Send email to doctor
    send_email_to_doctor(result)


def send_email_to_doctor(analysis):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = DOCTOR_EMAIL
        msg['Subject'] = "New Patient Analysis"

        body = f"A new patient analysis has been generated:\n\n{analysis}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, DOCTOR_EMAIL, text)
        server.quit()

        messagebox.showinfo("Success", "Analysis sent to doctor successfully!")
        print("Email sent to doctor successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")
        print(f"Error sending email: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("Patient Symptom Analyzer")
root.geometry("500x700")

# Create and place widgets
tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Age:").pack(pady=5)
age_entry = tk.Entry(root, width=40)
age_entry.pack()

tk.Label(root, text="Gender:").pack(pady=5)
gender_var = tk.StringVar()
gender_choices = ttk.Combobox(root, textvariable=gender_var, values=["Male", "Female", "Other"])
gender_choices.pack()

tk.Label(root, text="Location:").pack(pady=5)
location_entry = tk.Entry(root, width=40)
location_entry.pack()

tk.Label(root, text="Symptoms (comma-separated):").pack(pady=5)
symptoms_text = tk.Text(root, height=5, width=40)
symptoms_text.pack()

submit_button = tk.Button(root, text="Analyze Symptoms", command=get_possible_causes)
submit_button.pack(pady=10)

tk.Label(root, text="Analysis Result:").pack(pady=5)
result_text = tk.Text(root, height=15, width=50)
result_text.pack()

# Start the GUI event loop
root.mainloop()
