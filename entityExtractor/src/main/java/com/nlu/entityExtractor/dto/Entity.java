package com.nlu.entityExtractor.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 25/07/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Entity {

  private String value;
  private String name;

  public String getValue() {
    return value;
  }

  public void setValue(String value) {
    this.value = value;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }
}
