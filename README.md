# FTL modding: See a weapon's description on the main HUD.
**Note:** Not valid for FTL 1.6.1+. The junk character is no longer needed and only a new line is needed. It also seems that new lines via the new line character \n can be implemented by referring to <text> elements in text\_blueprints.xml

This readme and program assume you are familiar with Advanced Slipstream tags and creating mods with proper folder hierarchy and whatnot.

For use with FTL: Faster Than Light blueprints.xml-type files.

As you may know, weapons on FTL's in-game HUD only show stats. But what if you wanted to see the description there too? :wink:

Takes in a file full of weaponBlueprints and outputs slipstream tags that place the desc of the weaponBlueprint into its flavorType field (uses a technique to create paragraph structure, see image linked below).

For example, given a weaponBlueprint with a desc:
```
<weaponBlueprint name="BA_CRYSTAL_LIGHT_1">
	<desc>Modified projectile weapon that fires 3 shield piercing antipersonnel crystals. Cannot damage ships' structural integrity or deplete shields.</desc>
</weaponBlueprint>
```

Results in this generated:
```
<mod:findName type="weaponBlueprint" nname="BA_CRYSTAL_LIGHT_1">
	<mod-overwrite:flavorType>Modified projectile weapon that fires 3 shield piercing antipersonnel crystals. a
Cannot damage ships' structural integrity or deplete shields.</mod-overwrite:flavorType>
</mod:findName>
```

What it looks like in-game: https://i.imgur.com/SRqlDci.png

***Additional Notes:***

If desc has forced "paragraph" structure, this program will probably not generate the intended result.

Source file must have a proper root element and not be malformed in any other way -- FTL's files in general ignore this, but you need to make sure the file isn't malformed otherwise parsing will fail.

