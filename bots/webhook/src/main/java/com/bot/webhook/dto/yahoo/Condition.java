package com.bot.webhook.dto.yahoo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 29/06/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Condition {

  private String text;

  private String temp;

  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public String getTemp() {
    return temp;
  }

  public void setTemp(String temp) {
    this.temp = temp;
  }

  @Override
  public String toString() {
    return "Condition{" +
        "text='" + text + '\'' +
        ", temp='" + temp + '\'' +
        '}';
  }
}
