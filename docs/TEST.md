# Software Test Document

## 1. Introduction

### Project Overview

Sweet Potato adalah platform reviu aplikasi permainan, khususnya yang merupakan karya anak bangsa untuk pemain gim maupun pegiat gim. Platform ini bertujuan untuk dijadikan pusat informasi gim Indonesia yang menarik dan dapat meningkatkan lalu lintas pasar industri gim nasional.

### Purpose of Testing

Tujuan dari dokumen pengujian perangkat lunak ini adalah sebagai upaya penjaminan dan pengendali kualitas perangkat lunak pra- dan pascarilis. Platform Sweet Potato harus dipastikan layak untuk dipublikasi dan digunakan oleh khalayak umum serta mampu memberikan kontribusi nyata terhadap permasalahan.

### References

- Software Design Document

---

## 2. Test Plan

### Test Objectives

Pengujian perlu mengeksplor fungsionalitas sistem ketika dihadapkan pada kasus-kasus uji yang mungkin terjadi dalam lingkungan production.

### Scope of Testing

- **Included:** Fitur yang berkaitan dengan aplikasi permainan atau gim beserta informasi lain yang berkaitan.
- **Excluded:** Performa dan keamanan tidak akan dibahas dalam dokumen ini.

### Test Strategy

- Strategi pengujian menggabungkan pendekatan automation dan manual testing.

### Roles and Responsibilities

- **Tester:** Billdan | Back-end Developer, Nagym | Project Manager
- **Reviewer:** Gumarang | Front-end Developer.

### Schedule

| **Activity**        | **Start Date** | **End Date**   |
|---------------------|----------------|----------------|
| Requirement Analysis | 2025-01-02     | 2025-01-02     |
| Test Case Design     | 2025-01-02     | 2025-01-02     |
| Test Execution       | 2025-01-02     | 2025-01-02     |
| Test Closure         | 2025-01-02     | 2025-01-02     |

### Entry and Exit Criteria

- **Entry:** Pengembangan sudah selesai.
- **Exit:** Seluruh test case selesai dieksekusi.

---

## 3. Requirement Traceability Matrix (RTM)

| **Requirement ID** | **Description** | **Test Case ID** | **Status** |
|--------------------|-----------------|------------------|------------|
| RQ-001             | Daftar sebagai pengguna baru | TC-001, TC-002, TC-003 | In Progress |
| RQ-002             | Masuk sebagai pengguna terdaftar | TC-004, TC-005 | In Progress |
| RQ-003             | Melihat daftar gim | TC-006 | In Progress |
| RQ-004             | Melihat daftar gim baru yang akan datang | TC-007 | Not Covered |
| RQ-005             | Melihat daftar gim baru rilis | TC-008 | In Progress |
| RQ-006             | Melihat daftar gim berdasarkan peringkat | TC-009 | In Progress |
| RQ-007             | Mencari gim berdasarkan nama | TC-010 | In Progress |
| RQ-008             | Mencari gim berdasarkan genre | TC-011 | Not Covered |
| RQ-009             | Mencari gim berdasarkan platform | TC-012 | Not Covered |
| RQ-010             | Menilai gim | TC-013 | In Progress |
| RQ-011             | Mereviu gim | TC-014 | In Progress |
| RQ-012             | Menambahkan gim | TC-015, TC-016 | In Progress |
| RQ-013             | Mengedit informasi gim | TC-017, TC-018 | In Progress |

---

## 4. Test Cases

| **Test Case ID** | **Test Case Description** | **Steps to Execute** | **Expected Result** | **Status** |
|------------------|---------------------------|----------------------|---------------------|-----------|
| TC-001 | Verifikasi registrasi dengan data valid | 1. Masukkan username dan password. 2. Klik "Register". | Pengguna berhasil berhasil terdaftar. | Fail |
| TC-002 | Verifikasi registrasi dengan data tidak valid | 1. Masukkan username tidak valid (cth. "user name"). 2. Klik "Register". | Pesan eror tampil untuk username tidak valid. | Fail |
| TC-003 | Verifikasi registrasi dengan data wajib diisi kosong | 1. Kosongkan satu atau lebih kolom. 2. Klik "Register". | Pesan eror tampil untuk kolom kosong. | Fail |
| TC-004 | Verifikasi masuk sebagai pengguna dengan kredensial valid | 1. Masukkan username dan password. 2. Klik "Login". | Pengguna berhasil masuk. | Fail |
| TC-005 | Verifikasi masuk sebagai pengguna dengan kredensial tidak valid | 1. Masukkan username atau password yang tidak sesuai. 2. Klik "Login". | Pesan eror tampil untuk kredensial yang tidak sesuai. | Fail |
| TC-006 | Verifikasi tampilan daftar gim | 1. Navigasi ke halaman "Games". | Daftar gim tersedia tampil. | Fail |
| TC-007 | Verifikasi tampilan gim baru yang akan datang | 1. Navigasi ke seksi "Upcoming Games". | Daftar gim baru yang akan datang tampil. | Fail |
| TC-008 | Verifikasi tampilan gim yang baru rilis | 1. Navigasi ke seksi "New Releases". | Daftar gim baru rilis tampil. | Fail |
| TC-009 | Verifikasi tampilan gim berdasarkan penilaian | 1. Navigasi ke seksi "Top Rated Games". | Daftar gim dengan skor penilaian terbaik tampil. | Fail |
| TC-010 | Verifikasi pencarian gim berdasarkan judul gim | 1. Masukkan nama gim ke dalam kolom pencarian. 2. Tekan "Search". | Gim-gim relevan dengan pencarian tampil. | Fail |
| TC-011 | Verifikasi pencarian gim berdasarkan genrenya | 1. Pilih genre dari daftar genre. 2. Tekan "Search". | Gim dengan genre relevan tampil. | Fail |
| TC-012 | Verifikasi pencarian gim berdasarkan platformnya | 1. Pilih platform dari daftar daftar platform. 2. Tekan "Search". | Gim dengan platform relevan tampil | Fail |
| TC-013 | Verifikasi aktivitas menilai gim | 1. Navigasi menuju halaman detail gim. 2. Nilai gim dengan skor antara 1 s.d. 5. 3. Tekan "Submit". | Penilaian tersimpan dan tampil. | Fail |
| TC-014 | Verifikasi aktivitas mereviu gim | 1. Navigasi menuju halaman detail gim. 2. Reviu gim 3. Tekan "Submit". | Reviu tersimpan dan tampil. | Fail |
| TC-015 | Verifikasi aktivitas menambahkan gim baru | 1. Klik "Add Game". 2. Masukkan informasi gim valid. 3. Tekan "Save". | Gim berhasil ditambahkan. | Fail |
| TC-016 | Verifikasi aktivitas menambahkan gim baru dengan kolom wajib diisi kosong | 1. Kosongkan kolom wajib diisi. 2. Tekan "Save". | Pesan eror tampil untuk kolom "Required" yang kosong. | Fail |
| TC-017 | Verifikasi aktivitas menyunting informasi gim | 1. Klik "Edit Game" untuk gim tertentu. 2. Ubah informasi. 3. Tekan "Save". | Informasi gim berhasil diubah. | Fail |
| TC-018 | Verifikasi aktivitas menyunting gim dengan data tidak valid | 1. Masukkan data tidak valid (cth. teks ke dalam kolom angka). 2. tekan "Save". | Pesan eror tampil untuk input tidak valid. | Fail |

---

## 5. Test Environment

### Environment Configuration

- **Hardware:** List hardware configurations.
- **Software:** List software, OS, and tools.
- **Access:** Credentials and access methods.

---

## 6. Test Execution and Defect Tracking

### Test Execution Report

| **Test Case ID** | **Status** | **Remarks**         |
|-------------------|------------|---------------------|
| TC-001           | Pass       | -                   |
| TC-002           | Fail       | Error message incorrect |

### Defect Log

| **Defect ID** | **Description**       | **Severity** | **Steps to Reproduce** | **Status**  |
|---------------|-----------------------|--------------|-------------------------|-------------|
| D-001         | Login button not working | High        | Click on login button   | Open        |

---

## 7. Test Summary

### Test Results Summary

| **Metric**             | **Value** |
|------------------------|-----------|
| Total Test Cases       | X         |
| Passed Test Cases      | X         |
| Failed Test Cases      | X         |
| Defects Found          | X         |

### Lessons Learned

- Observations and recommendations for future projects.
