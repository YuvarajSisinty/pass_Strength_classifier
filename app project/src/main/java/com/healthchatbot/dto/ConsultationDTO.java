package com.healthchatbot.dto;

import java.time.LocalDateTime;

public class ConsultationDTO {
    private Long id;
    private String symptoms;
    private String prescriptionSuggestion;
    private String imagePath;
    private String analysisResult;
    private String seriousnessRating;
    private String consultationType;
    private LocalDateTime createdAt;

    public ConsultationDTO() {}

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSymptoms() {
        return symptoms;
    }

    public void setSymptoms(String symptoms) {
        this.symptoms = symptoms;
    }

    public String getPrescriptionSuggestion() {
        return prescriptionSuggestion;
    }

    public void setPrescriptionSuggestion(String prescriptionSuggestion) {
        this.prescriptionSuggestion = prescriptionSuggestion;
    }

    public String getImagePath() {
        return imagePath;
    }

    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }

    public String getAnalysisResult() {
        return analysisResult;
    }

    public void setAnalysisResult(String analysisResult) {
        this.analysisResult = analysisResult;
    }

    public String getSeriousnessRating() {
        return seriousnessRating;
    }

    public void setSeriousnessRating(String seriousnessRating) {
        this.seriousnessRating = seriousnessRating;
    }

    public String getConsultationType() {
        return consultationType;
    }

    public void setConsultationType(String consultationType) {
        this.consultationType = consultationType;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}

