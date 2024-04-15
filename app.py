import tkinter as tk
from tkinter import messagebox
from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster(['localhost'])  # Assuming Cassandra is running on localhost
session = cluster.connect("dataspace")  # Connect to your keyspace

def is_valid_age(age):
    try:
        int(age)
        return True
    except ValueError:
        return False

def create_record():
    name = name_entry.get()
    age = age_entry.get()
    if name and age and is_valid_age(age):
        query = "INSERT INTO student (name, age) VALUES (?, ?)"
        session.execute(query, (name, int(age)))
        messagebox.showinfo("Success", "Record created successfully")
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both name and a valid age")
    read_records()

def read_records():
    query = "SELECT * FROM student"
    rows = session.execute(query)
    records_listbox.delete(0, tk.END)
    for row in rows:
        records_listbox.insert(tk.END, f"Name: {row.name}, Age: {row.age}")

def delete_record():
    name = name_entry.get()
    if name:
        query = "DELETE FROM student WHERE name = ?"
        session.execute(query, (name,))
        messagebox.showinfo("Success", f"Record for {name} deleted successfully")
        name_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter name to delete")
    read_records()

def update_record():
    selected_index = records_listbox.curselection()
    if selected_index:
        selected_record = records_listbox.get(selected_index)
        selected_name = selected_record.split(',')[0].split(': ')[1]
        new_name = name_entry.get()
        new_age = age_entry.get()
        if new_name and new_age and is_valid_age(new_age):
            query = "UPDATE student SET name = ?, age = ? WHERE name = ?"
            session.execute(query, (new_name, int(new_age), selected_name))
            messagebox.showinfo("Success", "Record updated successfully")
            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)
            read_records()
        else:
            messagebox.showerror("Error", "Please enter both name and a valid age")
    else:
        messagebox.showerror("Error", "Please select a record to update")


# Create GUI
root = tk.Tk()
root.title("User Application")
root.geometry("400x400")  # Set window size

# Styling
root.configure(bg="#f0f0f0")  # Background color

label_bg = "#d3d3d3"  # Label background color
entry_bg = "#ffffff"  # Entry background color

# Center align all widgets
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Labels
name_label = tk.Label(root, text="Name:", bg=label_bg)
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

age_label = tk.Label(root, text="Age:", bg=label_bg)
age_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Entry fields
name_entry = tk.Entry(root, bg=entry_bg)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

age_entry = tk.Entry(root, bg=entry_bg)
age_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Buttons
create_button = tk.Button(root, text="Create", command=create_record, bg="#90ee90")
create_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

update_button = tk.Button(root, text="Update", command=update_record, bg="#ffff99")
update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

delete_button = tk.Button(root, text="Delete", command=delete_record, bg="#ff6347")
delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Listbox for displaying records
records_listbox = tk.Listbox(root, height=10, width=40, bg=entry_bg)
records_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

read_records()
root.mainloop()
