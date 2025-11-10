package com.healthchatbot.service;

import com.healthchatbot.entity.Consultation;
import com.healthchatbot.entity.User;
import com.healthchatbot.repository.ConsultationRepository;
import com.healthchatbot.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ConsultationService {

    @Autowired
    private ConsultationRepository consultationRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private AIService aiService;

    private static final String UPLOAD_DIR = "uploads/";

    public Consultation createSymptomConsultation(String username, String symptoms) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isEmpty()) {
            throw new RuntimeException("User not found");
        }

        User user = userOpt.get();
        String prescription = aiService.analyzeSymptoms(symptoms);

        Consultation consultation = new Consultation();
        consultation.setUser(user);
        consultation.setSymptoms(symptoms);
        consultation.setPrescriptionSuggestion(prescription);
        consultation.setConsultationType("SYMPTOM");

        return consultationRepository.save(consultation);
    }

    public Consultation createImageConsultation(String username, MultipartFile file) throws IOException {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isEmpty()) {
            throw new RuntimeException("User not found");
        }

        User user = userOpt.get();

        // Save uploaded file
        String imagePath = saveUploadedFile(file);

        // Analyze image using AI service
        String analysis = aiService.analyzeImage(imagePath);
        String seriousness = aiService.getSeriousnessRating();

        Consultation consultation = new Consultation();
        consultation.setUser(user);
        consultation.setImagePath(imagePath);
        consultation.setAnalysisResult(analysis);
        consultation.setSeriousnessRating(seriousness);
        consultation.setConsultationType("IMAGE");

        return consultationRepository.save(consultation);
    }

    public List<Consultation> getConsultationHistory(String username) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isEmpty()) {
            throw new RuntimeException("User not found");
        }

        return consultationRepository.findByUserOrderByCreatedAtDesc(userOpt.get());
    }

    private String saveUploadedFile(MultipartFile file) throws IOException {
        // Create uploads directory if it doesn't exist
        Path uploadPath = Paths.get(UPLOAD_DIR);
        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        // Generate unique filename
        String originalFilename = file.getOriginalFilename();
        String extension = originalFilename != null && originalFilename.contains(".") 
            ? originalFilename.substring(originalFilename.lastIndexOf(".")) 
            : "";
        String uniqueFilename = UUID.randomUUID().toString() + extension;

        // Save file
        Path filePath = uploadPath.resolve(uniqueFilename);
        Files.write(filePath, file.getBytes());

        return UPLOAD_DIR + uniqueFilename;
    }
}

