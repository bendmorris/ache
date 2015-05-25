Ache is an asset pipeline automation utility. You can use it to write complex 
series of actions to transform raw assets into final products.


Hello World!
------------

To run Ache, you'll need to write an XML configuration file containing two 
things: **rules** and **actions**. Here's a simple example:

    <pipeline>
        <rules>
            <print text="$txt">
                <exec>echo {$txt}</exec>
            </print>
        </rules>
    
        <print text="Hello"/>
        <print text="world!"/>
    </pipeline>

In the `<rules>` section, a rule is defined: whenever a "print" node is found, 
we should bind the value of its "text" attribute to the variable $txt, then 
execute the shell command "echo $txt" (substituting the value of the variable.) 
We then have two actions, which match the "print" rule to echo "Hello" and 
"world!".


Additional Features
-------------------

A somewhat more involved example:

    <pipeline>
        <rules>
            <svg path="$svgPath">
                <png path="$pngPath" w="$w" h="$h | $w">
                    <depends source="$svgPath" target="$pngPath">
                        <exec>
                            inkscape -e {$pngPath} --export-width={$w} --export-height={$h} {$svgPath}
                            python -m alpha_bandaid {$pngPath}
                        </exec>
                    </depends>
                </png>
            </svg>
        </rules>

        <svg path="assets/graphics/box.svg">
            <png path="assets/graphics/box.png" w="256"/>
        </svg>
        <svg path="assets/graphics/button.svg">
            <png path="assets/graphics/button.png" w="256"/>
        </svg>

        <svg path="assets/graphics/coin.svg">
            <png path="assets/graphics-flash/coin.png" w="32"/>
            <png path="assets/graphics-native/coin.png" w="64"/>
        </svg>
    </pipeline>

This example uses Inkscape to convert SVGs into PNGs, then runs a script on the 
resulting PNG. It can generate multiple PNGs per input SVG by listing multiple 
<png> nodes. For square images, the "h" attribute is unnecessary as it defaults 
to the value of "w". Finally, the "depends" node will ensure that the rule is 
only run when the target (1) doesn't exist or (2) is older than the source file.

More to come, stay tuned!
