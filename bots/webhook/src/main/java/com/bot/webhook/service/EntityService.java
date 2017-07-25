package com.bot.webhook.service;

import java.util.LinkedHashMap;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

/**
 * Created by prokarma on 25/07/17.
 */
@Service
public class EntityService {

  private RestTemplate restTemplate;

  @Autowired
  public EntityService(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public LinkedHashMap<String, String> getEntites(String query, String intent) {
    List<LinkedHashMap<String, String>> list = this.restTemplate
        .getForObject("http://localhost:9002/getEntities?query=" + query + "&intent=" + intent,
            List.class);
    return list.get(0);
  }
}
