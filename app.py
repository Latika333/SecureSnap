from flask import Flask, render_template, request, redirect, url_for, session
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated database
users = {}
photos = [
    {'title': 'Nature Landscape', 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80': 'static/images/photo1.jpg', 'encryption': 'AES-256'},
    {'title': 'Data Dashboard', 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxpaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80': 'static/images/photo2.jpg', 'encryption': 'AES-256'}
]

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Home page
@app.route('/')
def home():
    return render_template('index.html', photos=photos)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        if username in users:
            return "User already exists."
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        if users.get(username) == password:
            session['user'] = username
            return redirect(url_for('home'))
        return "Invalid credentials"
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Upload new image (admin or authenticated users)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        image = request.files['image']
        if image:
            path = os.path.join('static/images', image.filename)
            image.save(path)
            photos.append({'title': title, 'url': path, 'encryption': 'AES-256'})
            return redirect(url_for('home'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

