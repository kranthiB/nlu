package com.nlu.entityExtractor.domain.weather;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

/**
 * Created by prokarma on 25/07/17.
 */
@Document(collection = "cities")
public class City {

  @Id
  private ObjectId id;

  @Field(value = "City")
  private String city;

  @Field(value = "State")
  private String state;

  @Field(value = "Type")
  private String type;

  public ObjectId getId() {
    return id;
  }

  public void setId(ObjectId id) {
    this.id = id;
  }

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getState() {
    return state;
  }

  public void setState(String state) {
    this.state = state;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }
}
