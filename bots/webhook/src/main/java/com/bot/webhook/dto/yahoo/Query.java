package com.bot.webhook.dto.yahoo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 29/06/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class Query {

  private Results results;

  public Results getResults() {
    return results;
  }

  public void setResults(Results results) {
    this.results = results;
  }

  @Override
  public String toString() {
    return "Query{" +
        "results=" + results +
        '}';
  }
}
