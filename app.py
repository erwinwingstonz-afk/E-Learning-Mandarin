from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS responden (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        nilai INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= STYLE =================
STYLE = """
<style>
body { font-family: Arial; margin: 20px; }
.container { max-width:700px; margin:auto; }

input, button {
    width:100%;
    padding:10px;
    margin-top:10px;
    font-size:18px;
}

.card {
    background:#f2f2f2;
    padding:15px;
    margin-bottom:15px;
    border-radius:10px;
}

/* pilihan kolom */
.option-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}

.option-box {
    border:1px solid #ccc;
    padding:10px;
    border-radius:10px;
}

.option-box:hover {
    background:#e6f7ff;
}

table {
    width:100%;
    border-collapse: collapse;
}

th, td {
    border:1px solid #ccc;
    padding:10px;
    text-align:center;
}
</style>
"""

# ================= LOGIN =================
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == "123":
            session["user"] = request.form.get("username")
            return redirect("/menu")
        else:
            return STYLE + "<h3>Login gagal</h3>"

    return STYLE + """
    <div class="container">
    <h2>Login</h2>
    <form method="post">
        <input name="username" placeholder="Nama">
        <input type="password" name="password" placeholder="Password">
        <button>Login</button>
    </form>
    </div>
    """

# ================= MENU =================
@app.route("/menu")
def menu():
    user = session.get("user","Guest")
    return STYLE + f"""
    <div class="container">
    <h2>Halo, {user}</h2>

    <a href="/materi"><button>Materi</button></a>
    <a href="/quiz"><button>Quiz</button></a>
    <a href="/hasil"><button>Data</button></a>
    </div>
    """

# ================= MATERI =================
@app.route("/materi")
def materi():
    return STYLE + """
    <div class="container">
    <h2>Materi</h2>

    <div class="card">你好 → Halo</div>
    <div class="card">谢谢 → Terima kasih</div>
    <div class="card">再见 → Sampai jumpa</div>
    <div class="card">吃饭 → Makan</div>
    <div class="card">喝 → Minum</div>
    <div class="card">对不起 → Maaf</div>
    <div class="card">不客气 → Sama-sama</div>
    <div class="card">多少钱 → Berapa harga</div>
    <div class="card">在哪里 → Di mana</div>
    <div class="card">学习 → Belajar</div>

    <a href="/menu"><button>Kembali</button></a>
    </div>
    """

# ================= QUIZ =================
@app.route("/quiz", methods=["GET","POST"])
def quiz():
    user = session.get("user","Guest")

    kunci = {
        "q1":"A","q2":"B","q3":"A","q4":"B","q5":"A",
        "q6":"B","q7":"B","q8":"B","q9":"B","q10":"A"
    }

    if request.method == "POST":
        score = 0
        for k in kunci:
            if request.form.get(k) == kunci[k]:
                score += 1

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("INSERT INTO responden (nama,nilai) VALUES (?,?)",(user,score))
        conn.commit()
        conn.close()

        return STYLE + f"""
        <div class="container">
        <h2>Hasil</h2>
        <h3>{user}</h3>
        <h3>Nilai: {score}/10</h3>
        <a href="/menu"><button>Kembali</button></a>
        </div>
        """

    return STYLE + """
    <div class="container">
    <h2>Quiz</h2>
    <form method="post">

    <div class="card">1. 你好?
    <div class="option-grid">
    <label class="option-box"><input type="radio" name="q1" value="A"> Halo</label>
    <label class="option-box"><input type="radio" name="q1" value="B"> Maaf</label>
    </div></div>

    <div class="card">2. 谢谢?
    <div class="option-grid">
    <label class="option-box"><input type="radio" name="q2" value="A"> Maaf</label>
    <label class="option-box"><input type="radio" name="q2" value="B"> Terima kasih</label>
    </div></div>

    <div class="card">3. 吃饭?
    <div class="option-grid">
    <label class="option-box"><input type="radio" name="q3" value="A"> Makan</label>
    <label class="option-box"><input type="radio" name="q3" value="B"> Minum</label>
    </div></div>

    <div class="card">4. 对不起?
    <div class="option-grid">
    <label class="option-box"><input type="radio" name="q4" value="A"> Halo</label>
    <label class="option-box"><input type="radio" name="q4" value="B"> Maaf</label>
    </div></div>

    <div class="card">5. 喝?
    <div class="option-grid">
    <label class="option-box"><input type="radio" name="q5" value="A"> Minum</label>
    <label class="option-box"><input type="radio" name="q5" value="B"> Tidur</label>
    </div></div>

    <button>Submit</button>
    </form>

    <a href="/menu"><button>Kembali</button></a>
    </div>
    """

# ================= DATA =================
@app.route("/hasil", methods=["GET","POST"])
def hasil():
    if request.method == "POST":
        if request.form.get("password") != "erwin50125108":
            return STYLE + "<h3>Password salah</h3>"

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        data = c.execute("SELECT * FROM responden").fetchall()
        conn.close()

        html = "<div class='container'><h2>Data</h2><table>"
        html += "<tr><th>Nama</th><th>Nilai</th><th>Aksi</th></tr>"

        for d in data:
            html += f"""
            <tr>
            <td>{d[1]}</td>
            <td>{d[2]}</td>
            <td>
            <form method='post' action='/hapus/{d[0]}'>
            <input type='password' name='password'>
            <button>Hapus</button>
            </form>
            </td>
            </tr>
            """

        html += "</table><br><a href='/menu'><button>Kembali</button></a></div>"
        return STYLE + html

    return STYLE + """
    <div class="container">
    <h2>Password Admin</h2>
    <form method="post">
        <input type="password" name="password">
        <button>Lihat</button>
    </form>
    </div>
    """

# ================= HAPUS =================
@app.route("/hapus/<int:id>", methods=["POST"])
def hapus(id):
    if request.form.get("password") != "erwin50125108":
        return STYLE + "<h3>Password salah</h3>"

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("DELETE FROM responden WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/hasil")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)