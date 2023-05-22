import TextAttribute from './TextAttribute';
import CheckboxAttribute from './CheckboxAttribute';
import TitleAttribute from './TitleAttribute';
//import CategoryAttribute from './CategoryAttribute';
import StackableProperties from './StackableProperties';

const AttributeTypeMap = {
  "text": TextAttribute,
  "checkbox": CheckboxAttribute,
  "title": TitleAttribute,
//  "category": CategoryAttribute,
  "solution": TextAttribute,
  "reward": TextAttribute,
  "stackable_properties": StackableProperties
  // ...
};

export default AttributeTypeMap;
