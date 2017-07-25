package com.bot.webhook.controller;

import com.bot.webhook.dto.intent.IntentResponseDto;
import com.bot.webhook.service.EntityService;
import com.bot.webhook.service.IntentService;
import com.bot.webhook.service.YahooService;
import java.util.HashMap;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by prokarma on 25/07/17.
 */
@RestController
@CrossOrigin(origins = "http://localhost:9000")
public class WebhookController {

  private IntentService intentService;

  private EntityService entityService;

  private YahooService yahooService;

  @Autowired
  public WebhookController(IntentService intentService,
      EntityService entityService, YahooService yahooService) {
    this.intentService = intentService;
    this.entityService = entityService;
    this.yahooService = yahooService;
  }

  @GetMapping("/webhook")
  public String processRequest(String query) {
    String response = "Not able to Understand";
    IntentResponseDto intentResponse = intentService.getIntent(query);
    String intent = intentResponse.getIntent().getName();
    if ("weather".equalsIgnoreCase(intent)) {
      HashMap<String, String> entities = entityService.getEntites(query, intent);
      if (!CollectionUtils.isEmpty(entities)) {
        String value = "";
        for (Map.Entry<String, String> entry : entities.entrySet()) {
          if ("value".equalsIgnoreCase(entry.getKey())) {
            value = entry.getValue();
          }
          if ("name".equalsIgnoreCase(entry.getKey()) && "city"
              .equalsIgnoreCase(entry.getValue())) {
            response = getResponseFromYahoo(value);
          }
        }
      }
    }
    return response;
  }

  private String getResponseFromYahoo(String cityName) {
    return yahooService.processYahooWeatherForeCastRequest(cityName);
  }
}
