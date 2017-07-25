package com.nlu.entityExtractor.controller;

import com.nlu.entityExtractor.domain.weather.City;
import com.nlu.entityExtractor.dto.Entity;
import com.nlu.entityExtractor.repository.weather.CityRepository;
import com.nlu.entityExtractor.service.weather.WeatherService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by prokarma on 25/07/17.
 */
@RestController
public class EntityExtractor {

  private WeatherService weatherService;

  @Autowired
  public EntityExtractor(WeatherService weatherService) {
    this.weatherService = weatherService;
  }

  @GetMapping("/getEntities")
  public List<Entity> retrieveEntities(String intent, String query) {
    List<Entity> entities = new ArrayList<>();
    if ("weather".equalsIgnoreCase(intent)) {
      entities = weatherService.retrieveEntities(query);
    }
    return entities;
  }


}
