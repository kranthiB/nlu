package com.bot.webhook.service;

import com.bot.webhook.dto.intent.IntentResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

/**
 * Created by prokarma on 25/07/17.
 */
@Service
public class IntentService {

  private RestTemplate restTemplate;

  @Autowired
  public IntentService(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public IntentResponseDto getIntent(String query) {
    return this.restTemplate
        .getForObject("http://localhost:5000/parse?q=" + query, IntentResponseDto.class);
  }
}
