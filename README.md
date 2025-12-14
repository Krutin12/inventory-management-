# 🏭 Factory Management System - Backend API

A comprehensive Factory Management System backend built with Flask, SQLAlchemy, and JWT authentication. This system provides complete management of orders, inventory, raw materials, and purchase orders with role-based access control.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security](#security)
- [Deployment](#deployment)

## ✨ Features

### Core Functionality
- ✅ **User Management** - Admin and Manager roles with JWT authentication
- ✅ **Order Management** - Complete order lifecycle tracking
- ✅ **Inventory Management** - Stock level monitoring and alerts
- ✅ **Raw Materials** - Raw material tracking and management
- ✅ **Purchase Orders** - PO creation and receiving workflow
- ✅ **Dashboard** - Real-time statistics and analytics
- ✅ **Activity Logging** - Complete audit trail
- ✅ **Reporting** - Comprehensive reports with filters

### Technical Features
- 🔐 JWT Token-based authentication
- 🛡️ Role-based access control (RBAC)
- 📊 RESTful API design
- 🗄️ SQLAlchemy ORM
- 📝 Comprehensive error handling
- 🔍 Activity logging and audit trail
- 📈 Dashboard statistics and charts
- 🎯 Data validation

## 🛠️ Technology Stack

- **Framework:** Flask 3.0.0
- **Database:** SQLAlchemy (SQLite/PostgreSQL/MySQL)
- **Authentication:** Flask-JWT-Extended
- **CORS:** Flask-CORS
- **ORM:** SQLAlchemy
- **Password Hashing:** Werkzeug

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd factory-management-backend