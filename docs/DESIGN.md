# Software Design Document

## Sweet Potato

| Version | Date | Description |
|-------|---------|-------------|
| 1.0 | 2024-10-20 | Draft pertama SDD. |

***

## Table of Contents

1. [Introduction](#1-introduction)
    1. [Overview](#11-overview)
    2. [Purpose](#12-purpose)
    3. [Scope](#13-scope)
    4. [References](#14-references)
2. [System Requirements](#2-system-requirements)
    1. [Functional Requirements](#21-functional-requirements)
    2. [Non-Functional Requirements](#22-non-functional-requirements)
3. [System Architecture](#3-system-architecture)
4. [Frontend Design](#4-frontend-design)
5. [Backend Design](#5-backend-design)
    1. [Database Design](#51-database-design)
    2. [API Design](#52-api-design)

***

## 1. Introduction

### 1.1 Overview

Industri game di Indonesia sedang mengalami perkembangan, bahkan Peraturan Presiden No. 19/2024, pemerintah Indonesia menunjukkan keseriusannya dalam mempercepat pengembangan industri gim lokal. Data Kementerian Perindustrian pada tahun 2020 menunjukkan baru 0,4% industri lokal yang berkecimpung di pasar game Tanah Air, artinya industri asing masih mendominasi pasar nasional.

### 1.2 Purpose

Mengakselerasi industri gim Indonesia.

### 1.3. Scope

Platform/forum reviu gim-gim Indonesia sesama gamers beserta kritikus.

### 1.4. References

- [Peraturan Presiden No. 19/2024](https://www.presiden.go.id/id/peraturan-presiden/peraturan-presiden-no-19-tahun-2024-tentang-percepatan-pengembangan-industri-game-lokal)
- [Data Kementerian Perindustrian](https://www.kemenperin.go.id/id/perusahaan-perindustrian/data-perindustrian/data-perindustrian)

***

## 2 System Requirements

### 2.1 Functional Requirements

![Use Case Diagram](./Use%20Case%20Diagram.png)

### 2.2 Non-Functional Requirements

- Memiliki UI mudah dipahami oleh End User.
- Memiliki tingkat learnability yang baik.
- Memiliki compatibility yang baik.
- Mudah diperbaharui.
- Mudah dilakukan maintenance.

***

## 3. System Architecture

![System Architecture Model](./System%20Architecture%20Model.png)

***

## 4. Frontend Design

***

## 5. Backend Design

### 5.1 Database Design

![Entity Relationship Diagram](./Entity%20Relationship%20Diagram.png)

### 5.2 API Design

[API Documentation](../openapi.json)
