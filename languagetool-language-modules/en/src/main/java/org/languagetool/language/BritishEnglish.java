/* LanguageTool, a natural language style checker 
 * Copyright (C) 2012 Marcin Miłkowski (http://www.languagetool.org)
 * 
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
 * USA
 */

package org.languagetool.language;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

import org.languagetool.Language;
import org.languagetool.UserConfig;
import org.languagetool.rules.Rule;
import org.languagetool.rules.en.BritishReplaceRule;
import org.languagetool.rules.en.MorfologikBritishSpellerRule;
import org.languagetool.rules.en.UnitConversionRuleImperial;

public class BritishEnglish extends English {

  @Override
  public String[] getCountries() {
    return new String[]{"GB"};
  }

  @Override
  public String getName() {
    return "English (GB)";
  }

  @Override
  public List<Rule> getRelevantRules(ResourceBundle messages, UserConfig userConfig, List<Language> altLanguages) throws IOException {
    List<Rule> rules = new ArrayList<>();
    rules.addAll(super.getRelevantRules(messages, userConfig, altLanguages));
    rules.add(new BritishReplaceRule(messages));
    rules.add(new MorfologikBritishSpellerRule(messages, this, userConfig, altLanguages));
    rules.add(new UnitConversionRuleImperial(messages));
    return rules;
  }

  @Override
  public int getPriorityForId(String id) {
    switch (id) {
      case "OXFORD_SPELLING_IZE":                     return -20;
      case "PROTOTYPE_OXFORD_SPELLING_ISATION_NOUNS": return -21;
      case "PROTOTYPE_OXFORD_SPELLING_ISE_VERBS":     return -22;
    }
    return 0;
  }
}
