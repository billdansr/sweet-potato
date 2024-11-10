## Sweet Potato

***

# Software Design Document

| Versi | Tanggal | Description |
|-------|---------|-------------|
| 1.0 | 2024-10-20 | Draft pertama SDD. |

***

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
    1. [Latar Belakang](#11-latar-belakang)
    2. [Tujuan](#12-tujuan)
    3. [Deskripsi Aplikasi](#13-deskripsi-aplikasi)
    4. [Asumsi dan Batasan](#14-asumsi-dan-batasan)
    5. [Referensi](#15-referensi)
    6. [Definisi Istilah](#16-definisi-istilah)
2. [Kebutuhan Sistem](#2-kebutuhan-sistem)
    1. [Kebutuhan Fungsional](#21-kebutuhan-fungsional)
    2. [Kebutuhan Non-Fungsional](#22-kebutuhan-non-fungsional)
3. [Arsitektur Sistem](#3-arsitektur-sistem)
4. [Frontend Design](#4-frontend-design)
5. [Backend Design](#5-backend-design)
    1. [Database Design](#51-database-design)
    2. [API Design](#52-api-design)

***

## 1. Pendahuluan

### 1.1 Latar Belakang

Industri game di Indonesia sedang mengalami perkembangan, bahkan Peraturan Presiden No. 19/2024, pemerintah Indonesia menunjukkan keseriusannya dalam mempercepat pengembangan industri gim lokal. Data Kementerian Perindustrian pada tahun 2020 menunjukkan baru 0,4% industri lokal yang berkecimpung di pasar game Tanah Air, artinya industri asing masih mendominasi pasar nasional.

### 1.2 Tujuan

Mengakselerasi industri gim Indonesia.

### 1.3. Deskripsi Aplikasi

Platform/forum reviu gim-gim Indonesia sesama gamers dan kritikus.

#### 1.4. Asumsi dan Batasan

- Tidak ada batasan pada jumlah user.
- Tidak ada batasan pada jumlah game yang dapat di-review.
- Tidak ada batasan pada jumlah user yang dapat me-review.

#### 1.5. Referensi

- [Peraturan Presiden No. 19/2024](https://www.presiden.go.id/id/peraturan-presiden/peraturan-presiden-no-19-tahun-2024-tentang-percepatan-pengembangan-industri-game-lokal)
- [Data Kementerian Perindustrian](https://www.kemenperin.go.id/id/perusahaan-perindustrian/data-perindustrian/data-perindustrian)

#### 1.6. Definisi Istilah

- **User**: Pengguna aplikasi.
- **End User**: Pengguna aplikasi yang mengonsumsi produk aplikasi.
- **Game**: Game yang dapat di-review.
- **Review**: Review dari pengguna ke game.
- **Kritikus**: Reviewer yang merupakan ahli dalam memberikan review.
- **Admin**: Pengguna yang dapat mengelola aplikasi.

***

## 2 Kebutuhan Sistem

### 2.1 Kebutuhan Fungsional

![Use Case Diagram](./Use%20Case%20Diagram.png)

### 2.2 Kebutuhan Non-Fungsional

- Memiliki UI mudah dipahami oleh End User.
- Memiliki tingkat learnability yang baik.
- Memiliki compatibility yang baik.
- Mudah diperbaharui.
- Mudah dilakukan maintenance.

***

## 3. Arsitektur Sistem

![System Architecture Model](./System%20Architecture%20Model.png)

***

## 4. Frontend Design

***

## 5. Backend Design

### 5.1 Database Design

![Entity Relationship Diagram](./Entity%20Relationship%20Diagram.png)

### 5.2 API Design
