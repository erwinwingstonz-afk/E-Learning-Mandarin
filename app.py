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

body{
    font-family:Arial;
    background:#f4f6f9;
    margin:0;
    padding:20px;
}

.container{
    max-width:950px;
    margin:auto;
}

.card{
    background:white;
    padding:25px;
    border-radius:20px;
    margin-bottom:20px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

h1,h2,h3{
    text-align:center;
}

input{
    width:100%;
    padding:14px;
    margin-top:10px;
    border-radius:10px;
    border:1px solid #ccc;
    font-size:18px;
}

button{
    width:100%;
    padding:14px;
    margin-top:15px;
    border:none;
    border-radius:12px;
    background:#4CAF50;
    color:white;
    font-size:20px;
    cursor:pointer;
}

button:hover{
    background:#43a047;
}

.menu-btn{
    margin-bottom:15px;
}

.materi-box{
    background:#eef7ff;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
    font-size:24px;
}

.quiz-box{
    background:#fafafa;
    padding:25px;
    border-radius:15px;
    margin-top:20px;
    font-size:28px;
    line-height:2;
}

.quiz-box input[type="radio"]{
    transform:scale(2);
    margin-right:15px;
}

table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}

th,td{
    border:1px solid #ccc;
    padding:12px;
    text-align:center;
    font-size:18px;
}

th{
    background:#4CAF50;
    color:white;
}

.delete-btn{
    background:red;
}

</style>
"""

# ================= LOGIN =================
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # PASSWORD LOGIN
        if password == "123":

            session["user"] = username

            return redirect("/menu")

        else:

            return STYLE + """
            <div class='container'>

                <div class='card'>

                    <h2>Password Login Salah</h2>

                    <a href="/">
                        <button>Kembali</button>
                    </a>

                </div>

            </div>
            """

    return STYLE + """
    <div class='container'>

        <div class='card'>

            <h1>E-Learning Mandarin</h1>

            <form method="post">

                <input type="text"
                       name="username"
                       placeholder="Masukkan Nama">

                <input type="password"
                       name="password"
                       placeholder="Masukkan Password">

                <button>Login</button>

            </form>

        </div>

    </div>
    """

# ================= MENU =================
@app.route("/menu")
def menu():

    user = session.get("user","Guest")

    return STYLE + f"""
    <div class='container'>

        <div class='card'>

            <h2>Selamat Datang, {user}</h2>

            <a href="/materi">
                <button class='menu-btn'>
                📘 Materi Mandarin
                </button>
            </a>

            <a href="/quiz">
                <button class='menu-btn'>
                📝 Quiz Mandarin
                </button>
            </a>

            <a href="/hasil">
                <button class='menu-btn'>
                📊 Data Responden
                </button>
            </a>

        </div>

    </div>
    """

# ================= MATERI =================
@app.route("/materi")
def materi():

    return STYLE + """
    <div class='container'>

        <div class='card'>

            <h2>📘 Materi Dasar Mandarin</h2>

            <div class='materi-box'>
            你好 (nǐ hǎo) = Halo
            </div>

            <div class='materi-box'>
            谢谢 (xiè xie) = Terima Kasih
            </div>

            <div class='materi-box'>
            再见 (zài jiàn) = Sampai Jumpa
            </div>

            <div class='materi-box'>
            对不起 (duì bu qǐ) = Maaf
            </div>

            <div class='materi-box'>
            不客气 (bú kè qi) = Sama-sama
            </div>

            <div class='materi-box'>
            吃 (chī) = Makan
            </div>

            <div class='materi-box'>
            喝 (hē) = Minum
            </div>

            <div class='materi-box'>
            学习 (xué xí) = Belajar
            </div>

            <div class='materi-box'>
            多少钱 (duō shǎo qián) = Berapa Harga
            </div>

            <div class='materi-box'>
            在哪里 (zài nǎ lǐ) = Di Mana
            </div>

            <a href="/menu">
                <button>Kembali</button>
            </a>

        </div>

    </div>
    """

# ================= QUIZ =================
@app.route("/quiz", methods=["GET","POST"])
def quiz():

    user = session.get("user","Guest")

    jawaban = {
        "q1":"A",
        "q2":"B",
        "q3":"A",
        "q4":"B",
        "q5":"A",
        "q6":"A",
        "q7":"B",
        "q8":"A",
        "q9":"B",
        "q10":"A"
    }

    if request.method == "POST":

        score = 0

        for j in jawaban:

            if request.form.get(j) == jawaban[j]:
                score += 1

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO responden (nama,nilai) VALUES (?,?)",
            (user,score)
        )

        conn.commit()
        conn.close()

        return STYLE + f"""
        <div class='container'>

            <div class='card'>

                <h2>Hasil Quiz</h2>

                <h3>Nama : {user}</h3>

                <h3>Nilai : {score}/10</h3>

                <a href="/menu">
                    <button>Kembali</button>
                </a>

            </div>

        </div>
        """

    return STYLE + """
    <div class='container'>

        <div class='card'>

            <h2>📝 Quiz Mandarin</h2>

            <form method="post">

                <div class='quiz-box'>
                    1. 你好 (nǐ hǎo) artinya?
                    <br><br>
                    <input type="radio" name="q1" value="A"> Halo
                    <br>
                    <input type="radio" name="q1" value="B"> Maaf
                </div>

                <div class='quiz-box'>
                    2. 谢谢 (xiè xie) artinya?
                    <br><br>
                    <input type="radio" name="q2" value="A"> Belajar
                    <br>
                    <input type="radio" name="q2" value="B"> Terima Kasih
                </div>

                <div class='quiz-box'>
                    3. 再见 (zài jiàn) artinya?
                    <br><br>
                    <input type="radio" name="q3" value="A"> Sampai Jumpa
                    <br>
                    <input type="radio" name="q3" value="B"> Minum
                </div>

                <div class='quiz-box'>
                    4. 对不起 (duì bu qǐ) artinya?
                    <br><br>
                    <input type="radio" name="q4" value="A"> Halo
                    <br>
                    <input type="radio" name="q4" value="B"> Maaf
                </div>

                <div class='quiz-box'>
                    5. 不客气 (bú kè qi) artinya?
                    <br><br>
                    <input type="radio" name="q5" value="A"> Sama-sama
                    <br>
                    <input type="radio" name="q5" value="B"> Belajar
                </div>

                <div class='quiz-box'>
                    6. 吃 (chī) artinya?
                    <br><br>
                    <input type="radio" name="q6" value="A"> Makan
                    <br>
                    <input type="radio" name="q6" value="B"> Tidur
                </div>

                <div class='quiz-box'>
                    7. 喝 (hē) artinya?
                    <br><br>
                    <input type="radio" name="q7" value="A"> Belajar
                    <br>
                    <input type="radio" name="q7" value="B"> Minum
                </div>

                <div class='quiz-box'>
                    8. 学习 (xué xí) artinya?
                    <br><br>
                    <input type="radio" name="q8" value="A"> Belajar
                    <br>
                    <input type="radio" name="q8" value="B"> Harga
                </div>

                <div class='quiz-box'>
                    9. 多少钱 (duō shǎo qián) artinya?
                    <br><br>
                    <input type="radio" name="q9" value="A"> Di Mana
                    <br>
                    <input type="radio" name="q9" value="B"> Berapa Harga
                </div>

                <div class='quiz-box'>
                    10. 在哪里 (zài nǎ lǐ) artinya?
                    <br><br>
                    <input type="radio" name="q10" value="A"> Di Mana
                    <br>
                    <input type="radio" name="q10" value="B"> Makan
                </div>

                <button>Submit Quiz</button>

            </form>

            <a href="/menu">
                <button>Kembali</button>
            </a>

        </div>

    </div>
    """

# ================= DATA RESPONDEN =================
@app.route("/hasil", methods=["GET","POST"])
def hasil():

    if request.method == "POST":

        password = request.form.get("password")

        if password != "erwin50125108":

            return STYLE + """
            <div class='container'>
                <div class='card'>
                    <h2>Password Admin Salah</h2>
                </div>
            </div>
            """

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        data = c.execute(
            "SELECT id,nama,nilai FROM responden"
        ).fetchall()

        conn.close()

        html = """
        <div class='container'>

            <div class='card'>

                <h2>📊 Data Responden</h2>

                <table>

                    <tr>
                        <th>Nama</th>
                        <th>Nilai</th>
                        <th>Aksi</th>
                    </tr>
        """

        for d in data:

            html += f"""
            <tr>
                <td>{d[1]}</td>
                <td>{d[2]}</td>

                <td>
                    <a href="/hapus/{d[0]}">
                        <button class='delete-btn'>
                        Hapus
                        </button>
                    </a>
                </td>
            </tr>
            """

        html += """

                </table>

                <a href='/menu'>
                    <button>Kembali</button>
                </a>

            </div>

        </div>
        """

        return STYLE + html

    return STYLE + """
    <div class='container'>

        <div class='card'>

            <h2>Password Admin</h2>

            <form method="post">

                <input type="password"
                       name="password"
                       placeholder="Masukkan Password Admin">

                <button>Lihat Data</button>

            </form>

        </div>

    </div>
    """

# ================= HAPUS DATA =================
@app.route("/hapus/<int:id>")
def hapus(id):

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM responden WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/hasil")

# ================= RUN =================
if __name__ == "__main__":
    app.run()