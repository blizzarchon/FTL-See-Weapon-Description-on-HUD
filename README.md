# FTL modding: place weaponBlueprint in flavorType -- see the description on the main HUD 
For use with FTL: Faster Than Light blueprints.xml-type files.

As you may know, weapons on FTL's in-game HUD only show stats. But what if you wanted to see the description there too? :wink:

Takes in a file full of weaponBlueprints and outputs slipstream tags that place the desc of the weaponBlueprint into its flavorType field (uses a technique to create paragraph structure, see image linked below).

For example, given a desc:
```
<desc>Modified projectile weapon that fires 3 shield piercing antipersonnel crystals. Cannot damage ships' structural integrity or deplete shields.</desc>
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

Will probably not work as intended if desc has forced "paragraph" structure.

Source file must have a proper root element -- FTL's files in general ignore this, but you need it here otherwise parsing doesn't work.

