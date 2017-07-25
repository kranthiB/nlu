package com.nlu.entityExtractor;

import com.nlu.entityExtractor.domain.weather.City;
import com.nlu.entityExtractor.repository.weather.CityRepository;
import java.util.List;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class EntityExtractorApplication {

  public static void main(String[] args) {
    SpringApplication.run(EntityExtractorApplication.class, args);
  }
}
