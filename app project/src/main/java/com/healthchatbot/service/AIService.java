package com.healthchatbot.service;

import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

@Service
public class AIService {

    private final Random random = new Random();

    private final List<String> commonPrescriptions = Arrays.asList(
        "Rest and hydration. Consider over-the-counter pain relievers like acetaminophen or ibuprofen if needed.",
        "Apply warm compress and take rest. Consult a doctor if symptoms persist beyond 3 days.",
        "Maintain good hygiene and keep the affected area clean and dry. Monitor for any changes.",
        "Increase fluid intake and maintain a balanced diet. Avoid irritants and allergens.",
        "Get adequate sleep (7-9 hours) and consider stress-reduction techniques. Monitor symptoms closely.",
        "Apply cold compress if there's swelling. Avoid scratching or rubbing the affected area.",
        "Consider antihistamines for allergic reactions. Remove potential allergens from your environment.",
        "Over-the-counter antacids may help. Maintain a food diary to identify triggers.",
        "Gargle with warm salt water. Stay hydrated and get plenty of rest.",
        "Topical creams may provide relief. Keep the area clean and avoid tight clothing."
    );

    private final List<String> seriousnessLevels = Arrays.asList("Low", "Medium", "High");

    /**
     * Analyzes symptoms and returns a prescription suggestion
     */
    public String analyzeSymptoms(String symptoms) {
        if (symptoms == null || symptoms.trim().isEmpty()) {
            return "Please provide detailed symptoms for accurate analysis.";
        }

        String lowerSymptoms = symptoms.toLowerCase();
        
        // Simple keyword-based analysis (mocked AI logic)
        if (lowerSymptoms.contains("fever") && lowerSymptoms.contains("cough")) {
            return "Based on your symptoms of fever and cough, it's recommended to rest, stay hydrated, and monitor your temperature. If fever persists above 101°F (38.3°C) for more than 3 days, consult a healthcare provider. Over-the-counter fever reducers and cough suppressants may help. Note: This is a general suggestion - consult a doctor for proper diagnosis.";
        } else if (lowerSymptoms.contains("headache")) {
            return "For headaches, try resting in a dark, quiet room, stay hydrated, and consider over-the-counter pain relievers like ibuprofen or acetaminophen. If headaches are severe, frequent, or accompanied by vision changes, seek immediate medical attention.";
        } else if (lowerSymptoms.contains("rash") || lowerSymptoms.contains("itching")) {
            return "For skin rashes or itching, avoid scratching, keep the area clean and dry, and consider applying a gentle moisturizer or over-the-counter hydrocortisone cream. If the rash spreads, is painful, or accompanied by fever, consult a dermatologist.";
        } else if (lowerSymptoms.contains("stomach") || lowerSymptoms.contains("nausea")) {
            return "For stomach issues or nausea, stay hydrated with clear fluids, eat bland foods, avoid spicy or fatty foods, and rest. If symptoms persist or are severe, consult a healthcare provider.";
        } else {
            // Generic prescription based on random selection
            return commonPrescriptions.get(random.nextInt(commonPrescriptions.size())) + 
                   "\n\n⚠️ Important: This is an AI-generated suggestion and should not replace professional medical advice. Please consult a qualified healthcare provider for proper diagnosis and treatment.";
        }
    }

    /**
     * Analyzes an uploaded image and provides a seriousness rating
     * (Mock implementation - in a real app, this would use ML/AI APIs)
     */
    public String analyzeImage(String imagePath) {
        // Mock analysis - in reality, this would process the image using ML models
        String seriousness = seriousnessLevels.get(random.nextInt(seriousnessLevels.size()));
        
        String analysis = "AI Image Analysis Results:\n\n";
        
        if (seriousness.equals("Low")) {
            analysis += "Seriousness Rating: 🟢 LOW\n\n";
            analysis += "The uploaded image suggests minor concerns. The condition appears localized and manageable. ";
            analysis += "Recommendations: Monitor the area, maintain good hygiene, and apply appropriate over-the-counter treatments. ";
            analysis += "If the condition persists or worsens, consult a healthcare provider.";
        } else if (seriousness.equals("Medium")) {
            analysis += "Seriousness Rating: 🟡 MEDIUM\n\n";
            analysis += "The uploaded image indicates a condition that may require attention. ";
            analysis += "Recommendations: Keep the area clean, avoid irritants, and consider consulting a healthcare provider within 1-2 days if no improvement is seen. ";
            analysis += "Monitor for any signs of spreading or worsening symptoms.";
        } else {
            analysis += "Seriousness Rating: 🔴 HIGH\n\n";
            analysis += "The uploaded image suggests a condition that requires prompt medical attention. ";
            analysis += "Recommendations: Please consult a healthcare provider as soon as possible, preferably within 24 hours. ";
            analysis += "Do not delay seeking professional medical advice. If symptoms are severe or rapidly worsening, consider emergency care.";
        }
        
        analysis += "\n\n⚠️ Disclaimer: This AI analysis is for informational purposes only and does not constitute a medical diagnosis. Always consult a qualified healthcare professional for proper evaluation and treatment.";
        
        return analysis;
    }

    /**
     * Gets a seriousness rating for image analysis
     */
    public String getSeriousnessRating() {
        return seriousnessLevels.get(random.nextInt(seriousnessLevels.size()));
    }
}

