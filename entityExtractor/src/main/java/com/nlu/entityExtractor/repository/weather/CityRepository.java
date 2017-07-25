package com.nlu.entityExtractor.repository.weather;

import com.nlu.entityExtractor.domain.weather.City;
import java.util.List;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

/**
 * Created by prokarma on 25/07/17.
 */
@Repository
public interface CityRepository extends MongoRepository<City, Long> {

  List<City> findByCity(String city);

}
