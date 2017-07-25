package com.bot.webhook.service;

import com.bot.webhook.dto.yahoo.YahooResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

/**
 * Created by prokarma on 25/07/17.
 */
@Service
public class YahooService {

  private RestTemplate restTemplate;

  private String baseUrl = "https://query.yahooapis.com/v1/public/yql?";

  @Autowired
  public YahooService(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public String processYahooWeatherForeCastRequest(String cityName) {
    String yqlQuery = makeYqlQuery(cityName);
    String yqlUrl = baseUrl + "q=" + yqlQuery + "&format=json";

    HttpHeaders headers = new HttpHeaders();
    headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
    HttpEntity<?> httpEntity = new HttpEntity<>(headers);
    HttpEntity<YahooResponse> httpEntityResponse = restTemplate.exchange(yqlUrl,
        HttpMethod.GET, httpEntity, YahooResponse.class);
    YahooResponse yahooResponse = httpEntityResponse.getBody();
    String speech = "Today in " +
        yahooResponse.getQuery().getResults().getChannel().getLocation().getCity() +
        " : " +
        yahooResponse.getQuery().getResults().getChannel().getItem().getCondition().getText() +
        ", the temperature is " +
        yahooResponse.getQuery().getResults().getChannel().getItem().getCondition().getTemp() +
        " " +
        yahooResponse.getQuery().getResults().getChannel().getUnits().getTemperature();
    return speech;
  }

  private String makeYqlQuery(String cityName) {
    return "select * from weather.forecast where woeid in "
        + "(select woeid from geo.places(1) where text=\'"
        + cityName + "\')";
  }
}
