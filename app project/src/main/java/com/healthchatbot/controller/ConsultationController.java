package com.healthchatbot.controller;

import com.healthchatbot.dto.ConsultationDTO;
import com.healthchatbot.entity.Consultation;
import com.healthchatbot.service.ConsultationService;
import com.healthchatbot.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/consultations")
@CrossOrigin(origins = "*")
public class ConsultationController {

    @Autowired
    private ConsultationService consultationService;

    @Autowired
    private JwtUtil jwtUtil;

    private String extractUsernameFromToken(String token) {
        if (token != null && token.startsWith("Bearer ")) {
            token = token.substring(7);
        }
        return jwtUtil.extractUsername(token);
    }

    @PostMapping("/symptoms")
    public ResponseEntity<?> analyzeSymptoms(
            @RequestHeader("Authorization") String authHeader,
            @RequestBody SymptomRequest request) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Consultation consultation = consultationService.createSymptomConsultation(username, request.getSymptoms());
            return ResponseEntity.ok(convertToDTO(consultation));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error: " + e.getMessage());
        }
    }

    @PostMapping("/image")
    public ResponseEntity<?> analyzeImage(
            @RequestHeader("Authorization") String authHeader,
            @RequestParam("file") MultipartFile file) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Consultation consultation = consultationService.createImageConsultation(username, file);
            return ResponseEntity.ok(convertToDTO(consultation));
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error uploading file: " + e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error: " + e.getMessage());
        }
    }

    @GetMapping("/history")
    public ResponseEntity<?> getConsultationHistory(
            @RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            List<Consultation> consultations = consultationService.getConsultationHistory(username);
            List<ConsultationDTO> dtos = consultations.stream()
                    .map(this::convertToDTO)
                    .collect(Collectors.toList());
            return ResponseEntity.ok(dtos);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error: " + e.getMessage());
        }
    }

    private ConsultationDTO convertToDTO(Consultation consultation) {
        ConsultationDTO dto = new ConsultationDTO();
        dto.setId(consultation.getId());
        dto.setSymptoms(consultation.getSymptoms());
        dto.setPrescriptionSuggestion(consultation.getPrescriptionSuggestion());
        dto.setImagePath(consultation.getImagePath());
        dto.setAnalysisResult(consultation.getAnalysisResult());
        dto.setSeriousnessRating(consultation.getSeriousnessRating());
        dto.setConsultationType(consultation.getConsultationType());
        dto.setCreatedAt(consultation.getCreatedAt());
        return dto;
    }

    // Inner class for request body
    static class SymptomRequest {
        private String symptoms;

        public String getSymptoms() {
            return symptoms;
        }

        public void setSymptoms(String symptoms) {
            this.symptoms = symptoms;
        }
    }
}

