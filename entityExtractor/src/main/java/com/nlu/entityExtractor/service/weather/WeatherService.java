package com.nlu.entityExtractor.service.weather;

import com.nlu.entityExtractor.domain.weather.City;
import com.nlu.entityExtractor.dto.Entity;
import com.nlu.entityExtractor.repository.weather.CityRepository;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

/**
 * Created by prokarma on 25/07/17.
 */
@Service
public class WeatherService {

  private CityRepository cityRepository;

  @Autowired
  public WeatherService(CityRepository cityRepository) {
    this.cityRepository = cityRepository;
  }

  public List<Entity> retrieveEntities(String query) {
    List<Entity> entities = new ArrayList<>();
    String[] words = query.split(" ");
    final String[] entity = {""};
    Arrays.asList(words).forEach(word -> {
      List<City> cities = this.cityRepository.findByCity(word);
      if (!CollectionUtils.isEmpty(cities) && cities.size() > 0) {
        entity[0] = word;
      }
    });
    if (!"".equalsIgnoreCase(entity[0])) {
      Entity cityEntity = new Entity();
      cityEntity.setName("city");
      cityEntity.setValue(entity[0]);
      entities.add(cityEntity);
    }
    return entities;
  }
}
