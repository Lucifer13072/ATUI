def apply_styles(component, styles):
    component_type = component.__class__.__name__.lower()
    style = styles.get(component_type, {})
    
    # Применяем стиль к атрибутам компонента
    for key, value in style.items():
        component.attributes[key] = value

    # Рекурсивно применяем стили к дочерним элементам
    for child in component.children:
        apply_styles(child, styles)
