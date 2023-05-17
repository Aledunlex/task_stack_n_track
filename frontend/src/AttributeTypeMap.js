import TextAttribute from './AttributeComponents/TextAttribute';
import CheckboxAttribute from './AttributeComponents/CheckboxAttribute';
import TitleAttribute from './AttributeComponents/TitleAttribute';
//import CategoryAttribute from './AttributeComponents/CategoryAttribute';

const AttributeTypeMap = {
  "text": TextAttribute,
  "checkbox": CheckboxAttribute,
  "title": TitleAttribute,
//  "category": CategoryAttribute,
  "solution": TextAttribute,
  "reward": TextAttribute
  // ...
};

export default AttributeTypeMap;
