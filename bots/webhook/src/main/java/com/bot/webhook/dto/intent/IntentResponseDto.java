package com.bot.webhook.dto.intent;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by prokarma on 25/07/17.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class IntentResponseDto {

  private Intent intent;

  public Intent getIntent() {
    return intent;
  }

  public void setIntent(Intent intent) {
    this.intent = intent;
  }
}
