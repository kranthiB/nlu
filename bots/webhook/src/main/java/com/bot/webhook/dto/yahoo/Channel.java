package com.bot.webhook.dto.yahoo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 29/06/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Channel {

  private Location location;

  private Units units;

  private Item item;

  public Location getLocation() {
    return location;
  }

  public void setLocation(Location location) {
    this.location = location;
  }

  public Units getUnits() {
    return units;
  }

  public void setUnits(Units units) {
    this.units = units;
  }

  public Item getItem() {
    return item;
  }

  public void setItem(Item item) {
    this.item = item;
  }

  @Override
  public String toString() {
    return "Channel{" +
        "location=" + location +
        ", units=" + units +
        '}';
  }
}
