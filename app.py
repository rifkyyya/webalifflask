from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector

app = Flask(__name__)

#koneksi sql
db = connector.connect(
    host    = 'localhost',
    user    = 'root',
    passwd  = '',
    database= 'db_berita'
)

if db.is_connected():
    print('open connection successful')

@app.route('/')
def halaman_awal():
    cursor = db.cursor()
    cursor.execute('SELECT * from tbl_berita ORDER BY `tbl_berita`.`tanggal` desc LIMIT 0 , 4')
    result = cursor.fetchall()
    cursor.close()
    return render_template('index.html', hasil = result)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    tanggal = request.form['tanggal']
    judul = request.form['judul']
    isi = request.form['isi']
    cur = db.cursor()
    cur.execute('INSERT INTO tbl_berita (tanggal,judul,isi) VALUES (%s, %s, %s)', (tanggal,judul,isi))
    db.commit()
    return redirect(url_for('halaman_awal'))

@app.route('/ubah/<id>', methods=['GET'])
def ubah_data(id):
    cur = db.cursor()
    cur.execute('select * from tbl_berita where id=%s', (id,))
    res = cur.fetchall()
    cur.close()
    return render_template('edit.html', hasil = res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
	id = request.form['id']
	tanggal = request.form['edit_tanggal']
	judul = request.form['edit_judul']
	isi = request.form['edit_isi']
	cur = db.cursor()
	sql = "UPDATE tbl_berita SET tanggal=%s, judul=%s, isi=%s WHERE id=%s"
	value = (tanggal,judul,isi,id)
	cur.execute(sql, value)
	db.commit()
	return redirect(url_for('halaman_awal'))

@app.route('/hapus/<id>', methods=['GET'])
def hapus_data(id):
    cur = db.cursor()
    cur.execute('DELETE from tbl_berita where id=%s', (id,))
    db.commit()
    return redirect(url_for('halaman_awal'))

if __name__ == '__main__':
    app.run()
