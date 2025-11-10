package com.healthchatbot.repository;

import com.healthchatbot.entity.Consultation;
import com.healthchatbot.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ConsultationRepository extends JpaRepository<Consultation, Long> {
    List<Consultation> findByUserOrderByCreatedAtDesc(User user);
}

