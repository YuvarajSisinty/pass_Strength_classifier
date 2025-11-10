package com.healthchatbot.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "consultations")
public class Consultation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "symptoms", columnDefinition = "TEXT")
    private String symptoms;

    @Column(name = "prescription_suggestion", columnDefinition = "TEXT")
    private String prescriptionSuggestion;

    @Column(name = "image_path")
    private String imagePath;

    @Column(name = "analysis_result", columnDefinition = "TEXT")
    private String analysisResult;

    @Column(name = "seriousness_rating")
    private String seriousnessRating; // e.g., "Low", "Medium", "High"

    @Column(name = "consultation_type")
    private String consultationType; // "SYMPTOM" or "IMAGE"

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    public Consultation() {
        this.createdAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
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

