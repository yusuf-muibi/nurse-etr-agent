# 🏥 Nurse ETR Assistant - AI Healthcare Agent

An intelligent AI agent that automates nursing tasks in Electronic Treatment Records (ETR) systems, integrated with Telex.im for seamless communication.

## 🎯 Features

- **Patient Registration**: Automatically generate unique patient IDs
- **Vitals Recording**: Track blood pressure, temperature, pulse, respiratory rate, SpO2
- **Diagnosis Management**: Record doctor diagnoses
- **Medication Tracking**: Prescribe medications with automated reminders
- **Appointment Scheduling**: Schedule and track follow-up appointments
- **Smart Reminders**: Automated medication and appointment reminders
- **Natural Language Processing**: Interact using everyday language

## 🚀 Tech Stack

- **Backend**: Python FastAPI
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **AI/NLP**: Google Gemini AI
- **Scheduling**: APScheduler
- **Integration**: Telex.im API
- **Deployment**: Railway.app

## 📋 Prerequisites

- Python 3.10+
- Google Gemini API Key
- Telex.im Bot Token
- Railway Account (for deployment)

## 🛠️ Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/yusuf-muibi/nurse-etr-agent
cd nurse-etr-agent
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key
TELEX_BOT_TOKEN=your_telex_bot_token
TELEX_API_URL=https://api.telex.im
DATABASE_URL=sqlite:///./nurse_etr.db
```

### 5. Run Application
```bash
uvicorn app.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs

## 💬 Usage Examples

### Register a New Patient
```
"New patient John Doe, 45 years old, male, phone 08012345678"
```
**Response**: Patient registered with ID PT1234

### Record Vitals
```
"Record vitals for PT1234: BP 120/80, temperature 37.5, pulse 72, SpO2 98%"
```

### Add Diagnosis
```
"Dr Smith diagnosed PT1234 with hypertension and prescribed medication"
```

### Prescribe Medication
```
"Prescribe amoxicillin 500mg three times daily for PT1234"
```

### Schedule Appointment
```
"Schedule follow-up for PT1234 tomorrow at 2pm"
```

### Query Patient Records
```
"Show me PT1234's complete records"
```

## 🏗️ Architecture
```
┌─────────────┐
│  Telex.im   │ (User Interface)
└──────┬──────┘
       │ Webhooks
       ▼
┌─────────────┐
│   FastAPI   │ (Agent Logic)
│   ┌─────┐   │
│   │  AI │   │ (Gemini NLP)
│   └─────┘   │
│   ┌─────┐   │
│   │ SQLite │ │ (Database)
│   └─────┘   │
│   ┌─────┐   │
│   │Sched│   │ (Reminders)
│   └─────┘   │
└─────────────┘
```

## 🚂 Deployment

### Railway Deployment

1. Push code to GitHub
2. Connect Railway to your repository
3. Add environment variables
4. Railway will auto-deploy

**Live URL**: `https://nurse-etr-agent.up.railway.app/`

### Environment Variables

Required variables in Railway:
- `GEMINI_API_KEY`
- `TELEX_BOT_TOKEN`
- `TELEX_API_URL`
- `DATABASE_URL`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/agent/message` | POST | Process agent messages |
| `/agent/health` | GET | Agent health status |
| `/webhook/telex` | POST | Telex webhook receiver |
| `/docs` | GET | Interactive API documentation |

## 🧪 Testing

### Test Locally
```bash
# Run tests
pytest

# Test specific endpoint
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -d '{"message": "New patient test", "user_id": "test"}'
```

### Test on Railway
```bash
curl -X POST https://nurse-etr-agent.up.railway.app/agent/message \
  -H "Content-Type: application/json" \
  -d '{"message": "New patient John Doe, 30 years old", "user_id": "nurse_001"}'
```

## 🔐 Security

- Environment variables for sensitive data
- Input validation using Pydantic
- Error handling for all operations
- Webhook signature verification (TODO)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file

## 👥 Author

Yusuf Muibi

Project Link: [https://github.com/yusuf-muibi/nurse-etr-agent](https://nurse-etr-agent.up.railway.app/)

## 🙏 Acknowledgments

- Built for HNG Internship Stage 3
- Telex.im for messaging platform
- Google Gemini for AI capabilities
- Railway for hosting

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact via Telex.im
- Email: muibiyusuf01@gmail.com