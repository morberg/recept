-- Replaces fractions, e.g. 1/2, with latex code \sfrac{1}{2}
-- Requires xfrac package

if FORMAT ~= 'latex' then
    return {}
end

function Str(elem)
    local match_fraction = "(%d%d*)/(%d%d*)"
    local replace_fraction = "\\sfrac{%1}{%2}"

    if string.match(elem.text, match_fraction) then
        text = elem.text:gsub(match_fraction, replace_fraction)
        return pandoc.RawInline('latex', text)
    else
        return nil
    end
end
