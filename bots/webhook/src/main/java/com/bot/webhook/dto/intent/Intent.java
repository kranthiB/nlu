package com.bot.webhook.dto.intent;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 25/07/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Intent {

  private double confidence;
  private String name;

  public double getConfidence() {
    return confidence;
  }

  public void setConfidence(double confidence) {
    this.confidence = confidence;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }
}
