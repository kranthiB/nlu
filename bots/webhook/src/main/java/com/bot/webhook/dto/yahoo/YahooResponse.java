package com.bot.webhook.dto.yahoo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 29/06/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class YahooResponse {

  private Query query;

  public Query getQuery() {
    return query;
  }

  public void setQuery(Query query) {
    this.query = query;
  }

  @Override
  public String toString() {
    return "Response{" +
        "query=" + query +
        '}';
  }
}
