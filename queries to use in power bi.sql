-- Número total de imóveis disponíveis para venda:
SELECT COUNT(*) AS TotalImoveisVenda
FROM properties
WHERE group_type = 'Sales';

-- Número total de imóveis disponíveis para alugar:
SELECT COUNT(*) AS TotalImoveisAluguel
FROM properties
WHERE group_type = 'Rents';

-- Imóveis a venda abaixo de R$500.000:
SELECT COUNT(*) AS TotalImoveisMenor
FROM properties
WHERE property_price < 500000
AND property_price NOTNULL;

-- Imóveis a venda entre R$500.000 e R$1.000.000:
SELECT COUNT(*) AS TotalImoveisEntre
FROM properties
WHERE property_price >= 500000 
AND property_price <= 1000000;

-- Imóveis a venda acima de R$1.000.000:
SELECT COUNT(*) AS TotalImoveisMaior
FROM properties
WHERE property_price > 1000000;

-- Tabela com preço médio por m² de cada categoria:
SELECT category_type, AVG(property_price / property_area_size) AS PrecoMedioPorMetroQuadrado
FROM properties
WHERE property_price NOTNULL
AND property_area_size NOTNULL
AND property_area_size > 0
GROUP BY category_type;

-- Gráfico em pizza com a quantidade de imóveis para venda por categoria:
SELECT category_type, COUNT(*) AS Quantidade
FROM properties
WHERE group_type = 'Sales'
GROUP BY category_type;

-- Gráfico em pizza com a quantidade de imóveis para alugar por categoria:
SELECT category_type, COUNT(*) AS Quantidade
FROM properties
WHERE group_type = 'Rents'
GROUP BY category_type;

-- Gráfico em barra com a quantidade de imóveis por cidade:
SELECT city_name, COUNT(*) AS Quantidade
FROM properties
GROUP BY city_name;
