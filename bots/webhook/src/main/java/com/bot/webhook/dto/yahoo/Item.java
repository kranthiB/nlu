package com.bot.webhook.dto.yahoo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 29/06/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Item {

  private Condition condition;

  public Condition getCondition() {
    return condition;
  }

  public void setCondition(Condition condition) {
    this.condition = condition;
  }

  @Override
  public String toString() {
    return "Item{" +
        "condition=" + condition +
        '}';
  }
}
