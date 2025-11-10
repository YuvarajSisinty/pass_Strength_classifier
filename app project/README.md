# AI Health Chatbot 🏥

A full-stack web application for AI-powered health consultations. Users can input symptoms, upload medical images, and receive AI-generated analysis and prescription suggestions.

## Features

- 🔐 **User Authentication**: Secure signup and login with JWT tokens
- 📝 **Symptom Analysis**: Describe your symptoms and get AI-powered prescription suggestions
- 📷 **Image Analysis**: Upload photos (e.g., skin conditions) for AI analysis with seriousness rating
- 📋 **Consultation History**: View all your past consultations and recommendations
- 🎨 **Modern UI**: Beautiful, responsive web interface

## Tech Stack

- **Backend**: Java Spring Boot 3.2.0
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Database**: H2 (in-memory, for demo) or MySQL (production)
- **Security**: Spring Security with JWT authentication
- **Build Tool**: Maven
- **Java Version**: 17+

## Project Structure

```
ai-health-chatbot/
├── src/
│   ├── main/
│   │   ├── java/com/healthchatbot/
│   │   │   ├── config/          # Security & CORS configuration
│   │   │   ├── controller/       # REST API controllers
│   │   │   ├── dto/              # Data Transfer Objects
│   │   │   ├── entity/           # JPA entities (User, Consultation)
│   │   │   ├── repository/       # Data repositories
│   │   │   ├── service/          # Business logic (Auth, AI, Consultation)
│   │   │   └── util/             # Utilities (JWT)
│   │   └── resources/
│   │       ├── static/
│   │       │   ├── css/          # Stylesheets
│   │       │   ├── js/           # JavaScript files
│   │       │   ├── index.html    # Home page
│   │       │   ├── login.html    # Login page
│   │       │   ├── signup.html   # Signup page
│   │       │   └── dashboard.html # Main dashboard
│   │       └── application.properties
│   └── test/
└── pom.xml
```

## Prerequisites

- Java 17 or higher
- Maven 3.6+
- (Optional) MySQL 8.0+ if you want to use MySQL instead of H2

## Installation & Setup

### 1. Clone or navigate to the project directory

```bash
cd "app project"
```

### 2. Build the project

```bash
mvn clean install
```

### 3. Run the application

```bash
mvn spring-boot:run
```

Or run the main class `AIHealthChatbotApplication` from your IDE.

### 4. Access the application

- **Web Interface**: http://localhost:8080
- **H2 Console** (for database inspection): http://localhost:8080/h2-console
  - JDBC URL: `jdbc:h2:mem:healthchatbotdb`
  - Username: `sa`
  - Password: (leave empty)

## Usage

1. **Sign Up**: Create a new account at `/signup.html`
2. **Login**: Log in with your credentials at `/login.html`
3. **Dashboard**: 
   - Enter symptoms in the "Symptom Analysis" section
   - Upload an image in the "Image Analysis" section
   - View your consultation history in the "Consultation History" tab

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Consultations (Requires Authentication)
- `POST /api/consultations/symptoms` - Analyze symptoms
- `POST /api/consultations/image` - Analyze uploaded image
- `GET /api/consultations/history` - Get consultation history

## Configuration

### Using MySQL instead of H2

Edit `src/main/resources/application.properties` and uncomment the MySQL configuration:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/healthchatbot?createDatabaseIfNotExist=true
spring.datasource.username=root
spring.datasource.password=yourpassword
spring.jpa.database-platform=org.hibernate.dialect.MySQLDialect
spring.jpa.hibernate.ddl-auto=update
```

Then comment out or remove the H2 configuration lines.

## AI Analysis (Mock Implementation)

The current implementation uses **mocked AI logic**:
- **Symptom Analysis**: Keyword-based analysis with predefined prescription suggestions
- **Image Analysis**: Random seriousness ratings (Low/Medium/High) with generic analysis text

**Note**: In a production environment, you would integrate with actual AI/ML services like:
- OpenAI GPT-4 for symptom analysis
- Google Cloud Vision API or AWS Rekognition for image analysis
- Medical diagnosis APIs

## Security Features

- Password encryption using BCrypt
- JWT token-based authentication
- CORS configuration for frontend communication
- Protected API endpoints

## File Uploads

Uploaded images are saved in the `uploads/` directory (created automatically). Make sure this directory has write permissions.

## Development Tips

- The application uses H2 in-memory database by default, so data is lost on restart
- For persistent data, switch to MySQL (see Configuration section)
- JWT tokens expire after 24 hours (configurable in `application.properties`)
- Enable H2 console in production at your own risk (currently enabled for demo)

## Important Disclaimer

⚠️ **This application is for demonstration purposes only. The AI analysis is mocked and should NEVER be used as a substitute for professional medical advice. Always consult qualified healthcare providers for medical diagnosis and treatment.**

## Troubleshooting

### Port 8080 already in use
Change the port in `application.properties`:
```properties
server.port=8081
```

### Database connection issues
- Check database credentials in `application.properties`
- Ensure MySQL is running (if using MySQL)
- Check firewall settings

### JWT token issues
- Clear browser localStorage if tokens become invalid
- Check token expiration settings

## License

This project is for educational/demonstration purposes.

## Contributing

Feel free to fork and enhance this project! Some ideas:
- Integrate real AI/ML APIs
- Add user profiles and settings
- Implement email notifications
- Add more sophisticated image analysis
- Create mobile app versions

